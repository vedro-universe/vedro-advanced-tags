from baby_steps import given, then, when
from pyparsing import ParseResults

from vedro_advanced_tags._grammar import AndTag, NotTag, OrTag, TagExpr, TagOperand

from ._utils import make_tag


def test_tag_operand():
    with given:
        tokens = ParseResults(["API"])

    with when:
        tag_operand = TagOperand("...", 0, tokens)

    with then:
        assert isinstance(tag_operand, TagExpr)
        assert repr(tag_operand) == "Tag(API)"


def test_and_operator():
    with given:
        tokens = ParseResults([
            [make_tag("API"), "and", make_tag("P0")]
        ])

    with when:
        and_operator = AndTag("...", 0, tokens)

    with then:
        assert isinstance(and_operator, TagExpr)
        assert repr(and_operator) == "AND(Tag(API), Tag(P0))"


def test_or_operator():
    with given:
        tokens = ParseResults([
            [make_tag("API"), "or", make_tag("P0")]
        ])

    with when:
        or_operator = OrTag("...", 0, tokens)

    with then:
        assert isinstance(or_operator, TagExpr)
        assert repr(or_operator) == "OR(Tag(API), Tag(P0))"


def test_not_operator():
    with given:
        tokens = ParseResults([
            ["not", make_tag("API")]
        ])

    with when:
        not_operator = NotTag("...", 0, tokens)

    with then:
        assert isinstance(not_operator, TagExpr)
        assert repr(not_operator) == "NOT(Tag(API))"
