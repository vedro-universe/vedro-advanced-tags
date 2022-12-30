from typing import Type, Union

from vedro.core import Dispatcher, Plugin, PluginConfig
from vedro.events import ArgParsedEvent, ArgParseEvent, StartupEvent

from ._matcher import TagMatcher

__all__ = ("VedroAdvancedTags", "VedroAdvancedTagsPlugin",)


class VedroAdvancedTagsPlugin(Plugin):
    def __init__(self, config: Type["VedroAdvancedTags"]) -> None:
        super().__init__(config)
        self._tags: Union[str, None] = None

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
            .listen(ArgParsedEvent, self.on_arg_parsed) \
            .listen(StartupEvent, self.on_startup)

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        event.arg_parser.add_argument("-t", "--tags", help="Set tags")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._tags = event.args.tags

    async def on_startup(self, event: StartupEvent) -> None:
        if self._tags is None:
            return

        self._matcher = TagMatcher(self._tags)
        async for scenario in event.scheduler:
            tags = list(getattr(scenario._orig_scenario, "tags", ()))
            if not self._matcher.match(tags):
                event.scheduler.ignore(scenario)


class VedroAdvancedTags(PluginConfig):
    plugin = VedroAdvancedTagsPlugin
