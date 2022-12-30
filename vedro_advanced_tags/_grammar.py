from abc import ABC, abstractmethod
from typing import Callable, List, cast

from pyparsing import Literal, ParseResults, Word, alphanums, infixNotation, opAssoc

__all__ = ("parse", "TagsType",
           "And", "Or", "Not",
           "Operand", "Operator",
           "Expr", "TagsType",)


TagsType = List[str]


class Expr(ABC):
    @abstractmethod
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        pass

    @abstractmethod
    def __call__(self, tags: TagsType) -> bool:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Operator(Expr):
    pass


class Operand(Expr):
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        self._value = tokens[0]

    def __repr__(self) -> str:
        return f"Operand({self._value})"

    def __call__(self, tags: TagsType) -> bool:
        return self._value in tags


class And(Operator):
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        self._left = tokens[0][0]
        self._right = tokens[0][-1]

    def __repr__(self) -> str:
        return f"AND({self._left}, {self._right})"

    def __call__(self, tags: TagsType) -> bool:
        return cast(bool, self._left(tags) and self._right(tags))


class Or(Operator):
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        self._left = tokens[0][0]
        self._right = tokens[0][-1]

    def __repr__(self) -> str:
        return f"OR({self._left}, {self._right})"

    def __call__(self, tags: TagsType) -> bool:
        return cast(bool, self._left(tags) or self._right(tags))


class Not(Operator):
    def __init__(self, orig: str, location: int, tokens: ParseResults) -> None:
        self._value = tokens[0][-1]

    def __repr__(self) -> str:
        return f"NOT({self._value})"

    def __call__(self, tags: TagsType) -> bool:
        return not self._value(tags)


_operand = Word(alphanums).setParseAction(Operand)
_grammar = infixNotation(_operand, [
    (Literal("not"), 1, opAssoc.RIGHT, Not),
    (Literal("and"), 2, opAssoc.LEFT, And),
    (Literal("or"), 2, opAssoc.LEFT, Or),
])


def parse(expr: str) -> Callable[[TagsType], bool]:
    return cast(Callable[[TagsType], bool], _grammar.parseString(expr)[0])
