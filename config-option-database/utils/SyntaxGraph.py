class SyntaxGraph():
    def __init__(self, paths):
        self.graph = self.build_syntax_graph(paths)

    def build_syntax_graph(self, paths):
        graph = {None:{}}
        for path in paths:
            insert_to = graph[None]
            for token in path:
                if token[0] == "'" and token[-1] == "'":
                    token = token[1:-1]
                if not token in insert_to.keys():
                    insert_to[token] = {}
                insert_to = insert_to[token]
        # from json import dumps
        # print(dumps(graph, indent=2))
        return graph

    def print_path(self, children=None, string=''):
        if children == None:
            children = self.graph[None]
        keys = children.keys()
        if len(keys) == 0:
            print(string)
        elif len(keys) == 1:
            child = list(keys)[0]
            string2 = string + ' ' + child
            self.print_path(children[child], string2)
        else:
            print(string)
            sorted_keys = list(children.keys())
            sorted_keys.sort()
            for child in sorted_keys:
                string2 = len(string)*' ' + ' ' + child
                self.print_path(children[child], string2)