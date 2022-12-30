from abc import ABC, abstractmethod

from ._grammar import TagsType, parse

__all__ = ("AdvancdedTagMatcher", "TagMatcher",)


class TagMatcher(ABC):
    def __init__(self, expr: str) -> None:
        self._expr = expr

    @abstractmethod
    def match(self, tags: TagsType) -> bool:
        pass


class AdvancdedTagMatcher(TagMatcher):
    def __init__(self, expr: str) -> None:
        super().__init__(expr)
        self._grammar = parse(expr)

    def match(self, tags: TagsType) -> bool:
        return self._grammar(tags)
