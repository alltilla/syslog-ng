from __future__ import annotations
from typing import Set, Tuple

from .exceptions import MergeException
from .utils import indent


class Option:
    def __init__(self, name: str = None, params: Set[Tuple[str, ...]] = None) -> None:
        self.__name = name if name is not None else ""
        self.__params = params if params is not None else set()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def params(self) -> Set[Tuple[str, ...]]:
        return self.__params

    def copy(self) -> Option:
        copied = Option(self.name, set())
        copied.__params = self.__params.copy()

        return copied

    def merge(self, other: Option) -> None:
        if self.name != other.name:
            raise MergeException(
                "Cannot merge Options with different names: '{}' and '{}'".format(self.name, other.name)
            )

        self.__params |= other.__params

    def __repr__(self) -> str:
        return "Option({}, {})".format(repr(self.name), repr(self.params))

    def __named_option_str(self) -> str:
        string = "{}(".format(self.__name)

        if len(self.__params) == 0:
            string += ")"
        elif len(self.__params) == 1:
            string += " ".join(list(self.__params.copy())[0]) + ")"
        else:
            for params in sorted(self.__params):
                string += "\n{}".format(indent(" ".join(params)))
            string += "\n)"

        return string

    def __positional_option_str(self) -> str:
        string = ""

        for params in sorted(self.params):
            string += " ".join(params) + "\n"

        string = string[:-1]

        return string

    def __str__(self) -> str:
        if self.name != "":
            return self.__named_option_str()

        return self.__positional_option_str()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Option):
            return False

        return self.__name == other.__name and self.__params == other.__params
