__INDENTATION = 4


def indent(string: str) -> str:
    lines = string.split("\n")
    indented_lines = ["{}{}".format(" " * __INDENTATION, line) for line in lines]
    return "\n".join(indented_lines)
