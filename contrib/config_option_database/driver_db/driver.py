from __future__ import annotations

from .exceptions import MergeException
from .block import Block


class Driver(Block):
    def __init__(self, context: str, name: str) -> None:
        self.__context = context
        super().__init__(name)

    @property
    def context(self) -> str:
        return self.__context

    def copy(self) -> Driver:
        copied = Driver(self.context, self.name)
        copied.merge(self)

        return copied

    def merge(self, other: Block) -> None:
        if isinstance(other, Driver) and self.context != other.context:
            raise MergeException(
                "Cannot merge two drivers with different contexts: '{}' and '{}'".format(self.context, other.context)
            )

        super().merge(other)

    def to_block(self) -> Block:
        block = Block(self.name)
        block.merge(self)

        return block

    def __repr__(self) -> str:
        block_repr = super().__repr__()
        return "Driver({}, {}".format(repr(self.context), block_repr[len("Block(") :])

    def __str__(self) -> str:
        return "{} {}".format(self.context, super().__str__())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Driver):
            return False

        return self.context == other.context and super().__eq__(other)
