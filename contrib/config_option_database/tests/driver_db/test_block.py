from driver_db.block import Block
from driver_db.exceptions import MergeException
from driver_db.option import Option

import pytest


def test_defaults() -> None:
    block = Block("block")

    assert block.name == "block"
    assert len(block.blocks) == 0
    assert len(block.options) == 0


def test_add_get_remove_option() -> None:
    block = Block("block")
    block.add_option(Option("option", {("param-1-1", "param-1-2")}))
    block.add_option(Option("option", {("param-2-1", "param-2-2")}))
    block.add_option(Option(params={("param-3",)}))
    block.add_option(Option(params={("param-4",)}))

    assert len(block.options) == 2
    assert block.get_option("option") == Option("option", {("param-1-1", "param-1-2"), ("param-2-1", "param-2-2")})

    assert block.get_option("") == Option("", {("param-3",), ("param-4",)})

    block.remove_option("option")
    assert len(block.options) == 1
    with pytest.raises(KeyError):
        block.get_option("option")

    block.remove_option("")
    assert len(block.options) == 0
    with pytest.raises(KeyError):
        block.get_option("")


def test_add_get_remove_block() -> None:
    block = Block("block")

    inner_block_1 = Block("inner-block")
    inner_block_1.add_option(Option("option", {("param-1", "param-2")}))

    inner_block_2 = Block("inner-block")
    inner_block_2.add_option(Option("option", {("param-3", "param-4")}))

    block.add_block(inner_block_1)
    block.add_block(inner_block_2)

    expected_merged_inner_block = Block("inner-block")
    expected_merged_inner_block.add_option(Option("option", {("param-1", "param-2"), ("param-3", "param-4")}))

    assert len(block.blocks) == 1
    assert block.get_block("inner-block") == expected_merged_inner_block

    block.remove_block("inner-block")

    assert len(block.blocks) == 0
    with pytest.raises(KeyError):
        block.get_block("inner-block")


def test_eq() -> None:
    block_1 = Block("block")
    inner_block_1 = Block("inner-block")
    block_1.add_block(inner_block_1)
    block_1.add_option(Option("option", {("param-1",)}))

    block_2 = Block("block")
    inner_block_2 = Block("inner-block")
    block_2.add_block(inner_block_2)
    block_2.add_option(Option("option", {("param-1",)}))

    assert block_1 == block_2

    block_2.add_block(Block("inner-block-2"))

    assert block_1 != block_2

    assert block_1 != "not-a-Block-type"


def test_copy() -> None:
    block = Block("block")
    block.add_option(Option("option", {("param-1",)}))
    copied = block.copy()

    assert id(block) != id(copied)

    block.add_block(Block("inner-block"))
    block.add_option(Option("option", {("param-2",)}))

    assert len(block.blocks) == 1
    assert len(block.options) == 1
    assert block.get_block("inner-block") == Block("inner-block")
    assert block.get_option("option") == Option("option", {("param-1",), ("param-2",)})

    assert len(copied.blocks) == 0
    assert len(copied.options) == 1
    assert copied.get_option("option") == Option("option", {("param-1",)})


def test_merge() -> None:
    block_1 = Block("block")

    block_1.add_option(Option("option-1", {("param-1-1",)}))

    inner_block_1_1 = Block("inner-block-1")
    inner_block_1_1.add_option(Option("option-2", {("param-2-1",)}))
    block_1.add_block(inner_block_1_1)

    block_2 = Block("block")

    block_2.add_option(Option("option-1", {("param-1-2",)}))

    inner_block_1_2 = Block("inner-block-1")
    inner_block_1_2.add_option(Option("option-2", {("param-2-2",)}))
    block_2.add_block(inner_block_1_2)

    inner_block_2 = Block("inner-block-2")
    inner_block_2.add_option(Option(params={("param-3-1",)}))
    block_2.add_block(inner_block_2)

    expected_merged_block = Block("block")

    expected_merged_block.add_option(Option("option-1", {("param-1-1",), ("param-1-2",)}))

    expected_inner_block_1 = Block("inner-block-1")
    expected_inner_block_1.add_option(Option("option-2", {("param-2-1",), ("param-2-2",)}))
    expected_merged_block.add_block(expected_inner_block_1)

    expected_inner_block_2 = Block("inner-block-2")
    expected_inner_block_2.add_option(Option(params={("param-3-1",)}))
    expected_merged_block.add_block(expected_inner_block_2)

    block_1.merge(block_2)
    assert block_1 == expected_merged_block


def test_merge_different() -> None:
    block_1 = Block("block-1")
    block_2 = Block("block-2")

    with pytest.raises(MergeException):
        block_1.merge(block_2)


def test_repr() -> None:
    block = Block("block")
    block.add_block(Block("inner-block"))
    block.add_option(Option("option-1", {("param-1-1", "param-1-2")}))
    block.add_option(Option(params={("param-2-1",)}))

    assert (
        repr(block)
        == r"Block('block', {'inner-block': Block('inner-block', {}, {})}, {'option-1': Option('option-1', {('param-1-1', 'param-1-2')}), '': Option('', {('param-2-1',)})})"
    )


def test_str() -> None:
    block = Block("block")
    block.add_block(Block("inner-block"))
    block.add_option(Option(params={("positional-option-1",)}))
    block.get_block("inner-block").add_option(Option(params={("positional-option-2",)}))
    block.add_option(Option("a-option-1", {("param-1-1", "param-1-2")}))
    block.add_option(Option("option-2", {("param-2-1", "param-2-2")}))

    assert (
        str(block)
        == """
block(
    positional-option-1
    a-option-1(param-1-1 param-1-2)
    inner-block(
        positional-option-2
    )
    option-2(param-2-1 param-2-2)
)
""".strip()
    )
