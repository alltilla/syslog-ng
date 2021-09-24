import re
from pathlib import Path
from neologism import DCFG, Rule
from subprocess import check_output
from tempfile import NamedTemporaryFile, _TemporaryFileWrapper

from typing import Dict, List, Set

from driver_db import DriverDB, Block, Option
from .parse_sentence import parse_sentence, ParseError


class GrammarFileMissingError(Exception):
    pass


def __find_grammar_files(driver_source_dir: Path) -> Set[Path]:
    grammar_files = set(driver_source_dir.rglob("*-grammar.ym"))

    if len(grammar_files) == 0:
        raise GrammarFileMissingError()

    return grammar_files


def __merge_grammar_with_common_grammar(grammar_file: Path, merge_grammar_script: Path) -> _TemporaryFileWrapper:
    command = [str(merge_grammar_script), str(grammar_file)]
    merged_grammar = check_output(command)

    output_file = NamedTemporaryFile()
    output_file.write(merged_grammar)

    return output_file


def __format_types(grammar: DCFG) -> None:
    TYPES = (
        ("nonnegative_integer", "<nonnegative-integer>"),
        ("path", "<path>"),
        ("positive_integer", "<positive-integer>"),
        ("string", "<string>"),
        ("string_list", "<string-list>"),
        ("string_or_number", "<string-or-number>"),
        ("template_content", "<template-content>"),
        ("yesno", "<yesno>"),
        ("LL_ARROW", "=>"),
        ("LL_NUMBER", "<number>"),
        ("LL_FLOAT", "<float>"),
        ("LL_IDENTIFIER", "<identifier>"),
        ("LL_PLUGIN", "<plugin>"),
    )

    for type, formatted_type in TYPES:
        if type in grammar.symbols:
            grammar.make_symbol_terminal(type)
            grammar.add_rule(Rule(type, (formatted_type,)))


def __remove_ifdef(grammar: DCFG) -> None:
    for symbol in {"KW_IFDEF", "KW_ENDIF"}:
        if symbol in grammar.terminals:
            grammar.remove_symbol(symbol)


def __get_token_resolutions(parser_file: Path) -> Dict[str, Set[str]]:
    resolutions: Dict[str, Set[str]] = {}

    struct_regex = re.compile(r"CfgLexerKeyword[^;]*")
    entry_regex = re.compile(r"{[^{}]+,[^{}]+}")

    with parser_file.open("r") as f:
        for struct_match in struct_regex.finditer(f.read().replace("\n", "")):
            for entry_match in entry_regex.finditer(struct_match.group(0)):
                entry = entry_match.group(0)[1:-1].replace(" ", "").split(",")
                token = entry[1]
                keyword = entry[0][1:-1].replace("_", "-")
                resolutions.setdefault(token, set()).add(keyword)

    return resolutions


def __resolve_tokens_to_keywords(grammar: DCFG, common_parser_file: Path, parser_file: Path) -> None:
    parser_files: List[Path] = [common_parser_file, parser_file]
    for parser_file in parser_files:
        for token, resolutions in __get_token_resolutions(parser_file).items():
            for resolution in resolutions:
                grammar.add_rule(Rule(token, (resolution,)))


def __prepare_module_grammar(module_source_dir: Path, common_parser_file: Path, merge_grammar_script: Path) -> DCFG:
    module_grammar = DCFG()

    for grammar_file in __find_grammar_files(module_source_dir):
        parser_file = Path(str(grammar_file).replace("-grammar.ym", "-parser.c"))
        merged_grammar_file = __merge_grammar_with_common_grammar(grammar_file, merge_grammar_script)

        grammar = DCFG()
        grammar.load_yacc_file(merged_grammar_file.name)

        __format_types(grammar)
        __remove_ifdef(grammar)
        __resolve_tokens_to_keywords(grammar, common_parser_file, parser_file)

        module_grammar.load_dcfg(grammar)
        module_grammar.start_symbol = grammar.start_symbol

    return module_grammar


def __merge_blocks_and_options_with_the_same_name(driver_db: DriverDB) -> None:
    def process(block: Block):
        for option in list(block.options):
            try:
                inner_block_with_same_name = block.get_block(option.name)
            except KeyError:
                continue

            for params in option.params:
                inner_block_with_same_name.add_option(Option(params={params}))

            block.remove_option(option.name)

        for inner_block in block.blocks:
            process(inner_block)

    for ctx in driver_db.contexts:
        for driver in driver_db.get_drivers_in_context(ctx):
            process(driver)


def __connect_inner_plugins(driver_db: DriverDB) -> None:
    plugin_contexts = {
        "source": "inner-src",
        "destination": "inner-dest",
    }

    for ctx in driver_db.contexts:
        for driver in driver_db.get_drivers_in_context(ctx):
            try:
                option = driver.get_option("")
            except KeyError:
                continue

            if not ("<plugin>",) in option.params:
                continue

            if not ctx in plugin_contexts.keys():
                raise Exception("Plugin found for unexpected context: {}".format(ctx))  # TODO: special Exception

            try:
                plugin_drivers = driver_db.get_drivers_in_context(plugin_contexts[ctx])
            except KeyError:
                continue

            for plugin_driver in plugin_drivers:
                driver.add_block(plugin_driver.to_block())

            new_params = option.params
            new_params.remove(("<plugin>",))
            driver.remove_option("")
            if len(new_params) > 0:
                driver.add_option(Option(params=new_params))


def __post_process_driver_db(driver_db: DriverDB) -> None:
    __merge_blocks_and_options_with_the_same_name(driver_db)
    __connect_inner_plugins(driver_db)


def __load_drivers_in_module(module_source_dir: Path, common_parser_file: Path, merge_grammar_script: Path) -> DriverDB:
    drivers = DriverDB()

    try:
        grammar = __prepare_module_grammar(module_source_dir, common_parser_file, merge_grammar_script)
    except GrammarFileMissingError:
        print("    Skipping module: Grammar file is missing.\n")
        return DriverDB()

    for sentence in grammar.sentences:
        try:
            driver_slice = parse_sentence(sentence)
            drivers.add_driver(driver_slice)
        except ParseError as e:
            print("    Cannot parse sentence '{}': {}".format(" ".join(sentence), e))

    print()

    return drivers


def load_modules(lib_dir: Path, modules_dir: Path) -> DriverDB:
    common_parser_file = lib_dir / "cfg-parser.c"
    merge_grammar_script = lib_dir / "merge-grammar.py"

    driver_db = DriverDB()

    module_source_dirs: List[Path] = list(filter(lambda path: path.is_dir(), modules_dir.glob("*")))

    for module_source_dir in module_source_dirs:
        print("Loading module '{}'.".format(module_source_dir.name))

        drivers = __load_drivers_in_module(module_source_dir, common_parser_file, merge_grammar_script)
        driver_db.merge(drivers)

    __post_process_driver_db(driver_db)

    return driver_db
