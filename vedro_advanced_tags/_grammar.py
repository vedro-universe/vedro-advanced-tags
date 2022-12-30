from abc import ABC, abstractmethod
from typing import Callable, List, cast

from pyparsing import Literal, ParseResults, Word, alphanums, infixNotation, opAssoc

__all__ = ("parse", "TagsType",
           "AndTag", "OrTag", "NotTag",
           "TagOperand", "TagOperator",
           "TagExpr", "TagsType",)


TagsType = List[str]


class TagExpr(ABC):
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        pass

    @abstractmethod
    def __call__(self, tags: TagsType) -> bool:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class TagOperator(TagExpr):
    pass


class TagOperand(TagExpr):
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        super().__init__(orig, location, tokens)
        self._value = tokens[0]

    def __repr__(self) -> str:
        return f"Tag({self._value})"

    def __call__(self, tags: TagsType) -> bool:
        return self._value in tags


class AndTag(TagOperator):
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        super().__init__(orig, location, tokens)
        self._left = tokens[0][0]
        self._right = tokens[0][-1]

    def __repr__(self) -> str:
        return f"AND({self._left}, {self._right})"

    def __call__(self, tags: TagsType) -> bool:
        return cast(bool, self._left(tags) and self._right(tags))


class OrTag(TagOperator):
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        super().__init__(orig, location, tokens)
        self._left = tokens[0][0]
        self._right = tokens[0][-1]

    def __repr__(self) -> str:
        return f"OR({self._left}, {self._right})"

    def __call__(self, tags: TagsType) -> bool:
        return cast(bool, self._left(tags) or self._right(tags))


class NotTag(TagOperator):
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        super().__init__(orig, location, tokens)
        self._value = tokens[0][-1]

    def __repr__(self) -> str:
        return f"NOT({self._value})"

    def __call__(self, tags: TagsType) -> bool:
        return not self._value(tags)


_operand = Word(alphanums).setParseAction(TagOperand)
_grammar = infixNotation(_operand, [
    (Literal("not"), 1, opAssoc.RIGHT, NotTag),
    (Literal("and"), 2, opAssoc.LEFT, AndTag),
    (Literal("or"), 2, opAssoc.LEFT, OrTag),
])


def parse(expr: str) -> Callable[[TagsType], bool]:
    return cast(Callable[[TagsType], bool], _grammar.parseString(expr)[0])
