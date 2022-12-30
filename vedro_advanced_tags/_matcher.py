from ._grammar import TagsType, parse

__all__ = ("TagMatcher",)


class TagMatcher:
    def __init__(self, expr: str) -> None:
        self._expr = expr
        self._grammar = parse(expr)

    def match(self, tags: TagsType) -> bool:
        return self._grammar(tags)
