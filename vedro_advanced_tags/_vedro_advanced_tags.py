from typing import Any, Callable, Type, Union

from vedro.core import Dispatcher, Plugin, PluginConfig, VirtualScenario
from vedro.events import ArgParsedEvent, ArgParseEvent, CleanupEvent, StartupEvent

from ._tag_matcher import AdvancedTagMatcher, TagMatcher

__all__ = ("VedroAdvancedTags", "VedroAdvancedTagsPlugin",)


class VedroAdvancedTagsPlugin(Plugin):
    def __init__(self, config: Type["VedroAdvancedTags"], *,
                 tag_matcher_factory: Callable[[str], TagMatcher] = AdvancedTagMatcher) -> None:
        super().__init__(config)
        self._show_parsed = config.show_parsed
        self._matcher_factory = tag_matcher_factory
        self._matcher: Union[TagMatcher, None] = None
        self._tags: Union[str, None] = None

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
            .listen(ArgParsedEvent, self.on_arg_parsed) \
            .listen(StartupEvent, self.on_startup) \
            .listen(CleanupEvent, self.on_cleanup)

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        event.arg_parser.add_argument("-t", "--tags", help="Set tags")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._tags = event.args.tags

    def _validate_tags(self, scenario: VirtualScenario, tags: Any) -> bool:
        if not isinstance(tags, (list, tuple, set)):
            raise TypeError(f"Scenario '{scenario.rel_path}' tags must be a list, tuple or set, "
                            f"got {type(tags)}")

        for tag in tags:
            if not tag.isidentifier():
                raise ValueError(
                    f"Scenario '{scenario.rel_path}' tag '{tag}' is not a valid identifier")

        return True

    async def on_startup(self, event: StartupEvent) -> None:
        if self._tags is None:
            return

        self._matcher = self._matcher_factory(self._tags)
        async for scenario in event.scheduler:
            tags = getattr(scenario._orig_scenario, "tags", ())
            self._validate_tags(scenario, tags)
            if not self._matcher.match(list(tags)):
                event.scheduler.ignore(scenario)

    def on_cleanup(self, event: CleanupEvent) -> None:
        if self._tags and self._matcher and self._show_parsed:
            event.report.add_summary(
                f'--tags "{self._tags}" -> {self._matcher._grammar!r}')  # type: ignore


class VedroAdvancedTags(PluginConfig):
    plugin = VedroAdvancedTagsPlugin

    # Show parsed tags in summary
    show_parsed: bool = False
