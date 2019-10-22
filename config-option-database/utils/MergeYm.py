#!/usr/bin/env python3

from pathlib import Path
from sys import argv

def get_grammar_files():
    root_dir = Path(__file__).resolve().parents[2]
    files = list(root_dir.glob('**/*.ym'))
    files.append(root_dir.joinpath('lib/cfg-grammar.y'))
    return files

def skip_filepath(filepath):
    return 'plugin_template_grammar.ym' == filepath.name

def merge_grammars(output_filepath):
    files = get_grammar_files()
    declarations = set()
    blocks = r'%%' + '\n'

    for filepath in files[1:]:
        if skip_filepath(filepath):
            continue
        with filepath.open() as f:
            in_block = False
            for line in f:
                if line.startswith('%token') or line.startswith(r'%left') or line.startswith('%type'):
                    declarations.add(line)
                elif line.startswith(r'%%'):
                    in_block = not in_block
                elif in_block:
                    blocks += line
    blocks += r'%%' + '\n'

    with open(output_filepath, 'w') as f:
        f.write(''.join(declarations)+blocks)

def main():
    output_filepath = 'syslog-grammar-merged.y'
    if len(argv) >= 2:
        output_filepath = argv[1]

    merge_grammars(output_filepath)


if __name__ == '__main__':
    main()
