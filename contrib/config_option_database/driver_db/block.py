from __future__ import annotations
from typing import Dict, ValuesView

from .exceptions import MergeException
from .option import Option
from .utils import indent


class Block:
    def __init__(self, name: str):
        self.__name = name
        self.__blocks: Dict[str, Block] = dict()
        self.__options: Dict[str, Option] = dict()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def blocks(self) -> ValuesView[Block]:
        return self.__blocks.values()

    def get_block(self, name: str) -> Block:
        return self.__blocks[name]

    def add_block(self, block: Block) -> None:
        if not block.name in self.__blocks.keys():
            self.__blocks[block.name] = block.copy()
        else:
            self.get_block(block.name).merge(block)

    def remove_block(self, name) -> None:
        self.__blocks.pop(name)

    @property
    def options(self) -> ValuesView[Option]:
        return self.__options.values()

    def get_option(self, name: str) -> Option:
        return self.__options[name]

    def add_option(self, option: Option) -> None:
        if not option.name in self.__options.keys():
            self.__options[option.name] = option.copy()
        else:
            self.get_option(option.name).merge(option)

    def remove_option(self, name: str) -> None:
        self.__options.pop(name)

    def merge(self, other: Block) -> None:
        if self.name != other.name:
            raise MergeException(
                "Cannot merge two Blocks with different names: '{}' and '{}'".format(self.name, other.name)
            )

        for block in other.blocks:
            self.add_block(block)

        for option in other.options:
            self.add_option(option)

    def copy(self) -> Block:
        copied = Block(self.name)
        copied.merge(self)

        return copied

    def __repr__(self) -> str:
        return "Block({}, {}, {})".format(repr(self.__name), repr(self.__blocks), repr(self.__options))

    def __str__(self) -> str:
        string = "{}(\n".format(self.name)

        block_and_option_strs: Dict[str, str] = {}

        for block_name in sorted(self.__blocks.keys()):
            block_and_option_strs.setdefault(block_name, "")
            block_and_option_strs[block_name] += "{}\n".format(indent(str(self.get_block(block_name))))

        for option_name in sorted(self.__options.keys()):
            block_and_option_strs.setdefault(option_name, "")
            block_and_option_strs[option_name] += "{}\n".format(indent(str(self.get_option(option_name))))

        for block_or_option_name in sorted(block_and_option_strs.keys()):
            string += block_and_option_strs[block_or_option_name]

        string += ")"

        return string

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Block):
            return False

        return self.__name == other.__name and self.__blocks == other.__blocks and self.__options == other.__options
