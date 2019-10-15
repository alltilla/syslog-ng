from argparse import ArgumentParser
from pprint import pprint

def lines_append(lines, terminal):
    buf = lines[:]
    for i in range(len(lines)):
        if buf[i] != '':
            buf[i] += ' '
        buf[i] += terminal
    return buf

def get_lines(graph, node, stack, lines):
    if node in stack:
        return lines
    stack.append(node)

    if graph.is_junction(node):
        for child in graph.get_children(node):
            if graph.is_terminal(child):
                if child != graph.get_end() and '$@' != child[:2]:
                    lines = lines_append(lines, child)
            else:
                lines = get_lines(graph, child, stack, lines)
    else:
        new_lines = []
        for child in graph.get_children(node):
            new_line = get_lines(graph, child, stack, lines)
            new_lines.extend(new_line)
        lines = new_lines

    stack.pop()
    return lines

class OptionParser():
    def __init__(self, line, options):
        self.tokens = line.split(' ')
        self.options = options

    class Option():
        def __init__(self, drivers, keyword, types, parents):
            self.drivers = drivers
            self.keyword = keyword
            self.types = types
            self.parents = parents

    def _find_leaves(self):
        leaves = set()
        lb = None

        for index, token in enumerate(self.tokens):
            if token == "'('":
                lb = index
            elif token == "')'" and lb != None:
                assert self.tokens[lb-1][0:3] == 'KW_', "No KW_ before '('"
                leaves.add((lb-1, index))
                lb = None

        skip = 0
        lb = None
        for index in range(len(self.tokens)-1, 0, -1):
            token = self.tokens[index]
            if token == "'('":
                if skip:
                    skip -= 1
                    continue
                if lb and lb - index > 2:
                    leaves.add((index+1, lb-1-1))
                lb = index
            elif token == "')'" and lb:
                skip += 1

        return leaves

    def _get_options(self, leaves):
        assert self.tokens[0][:11] == 'LL_CONTEXT_'
        assert self.tokens[1][:3] == 'KW_'
        assert self.tokens[2] == "'('"
        options = []
        drivers = [(self.tokens[0], self.tokens[1])]
        for leave_interval in leaves:
            leave = self.tokens[leave_interval[0]:leave_interval[1]+1]
            if "'('" in leave and "')'" in leave:
                assert leave.index("'('") == 1
                assert leave.index("')'") == len(leave)-1
                assert leave[0][:3] == 'KW_'
                keyword = leave[0]
                types = leave[leave.index("'('")+1:leave.index("')'")]
            else:
                keyword = None
                types = leave

            skip = 0
            parents = []
            next_is_kw = False
            reverse_sublist = self.tokens[:leave_interval[0]]
            reverse_sublist.reverse()
            for token in reverse_sublist:
                if token == "'('":
                    if skip:
                        skip -= 1
                    else:
                        next_is_kw = True
                elif next_is_kw:
                    parents.append(token)
                    next_is_kw = False
                elif token == "')'":
                    skip += 1
            parents.reverse()
            parents = parents[1:]
            option = OptionParser.Option(drivers, keyword, types, parents)
            append = True
            for other in self.options:
                if option.keyword == other.keyword and option.types == other.types and option.parents == other.parents:
                    if option.drivers[0] not in other.drivers:
                        other.drivers.append(option.drivers[0])
                    append = False
                    break
            if append:
                options.append(option)
        return options

    def parse(self):
        leaves = self._find_leaves()
        options = self._get_options(leaves)
        return options

def get_options(graph):
    lines = get_lines(graph, graph.get_start(), [], [''])
    options = []
    for line in lines:
        option_parser = OptionParser(line, options)
        options.extend(option_parser.parse())
    return options

def cut_at_types(graph):
    types = [
        'date_parser_flags',
        'date_parser_stamp',
        'dnsmode',
        'facility_string',
        'filter_content',
        'filter_expr',
        'filter_fac_list',
        'filter_level_list',
        'http_auth_header_plugin',
        'inherit_mode',
        'level_string',
        'log_flags_items',
        'matcher_flags',
        'nonnegative_integer',
        'nonnegative_integer64',
        'parser_csv_delimiters',
        'parser_csv_dialect',
        'parser_csv_flags',
        'path_check',
        'path_no_check',
        'path_secret',
        'positive_integer',
        'stateful_parser_inject_mode',
        'string',
        'string_list',
        'string_or_number',
        'synthetic_message',
        'template_content',
        'template_content_inner',
        'vp_scope_list',
        'yesno',
    ]

    for opt_type in types:
        if not opt_type in graph.get_nodes():
            continue
        graph.make_terminal(opt_type)

def print_options(options):
    database = {}
    for option in options:
      contexts = set()
      for driver in option.drivers:
        contexts.add(driver[0])
      for context in contexts:
        entry = {}
        if option.keyword:
          entry['option_name'] = option.keyword
        else:
          entry['option_name'] = ''
        entry['option_value'] = option.types
        entry['parent_options'] = option.parents
        root_driver = []
        for driver in option.drivers:
          if driver[0] == context:
            root_driver.append(driver[1])
        entry['root_driver'] = root_driver
        if context not in database:
          database[context] = []
        database[context].append(entry)
    pprint(database)

def plugin(graph, args):
    cut_at_types(graph)
    options = get_options(graph)
    print_options(options)

