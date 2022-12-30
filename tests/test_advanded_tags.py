import pytest
from baby_steps import given, then, when
from vedro.core import Dispatcher
from vedro.core import MonotonicScenarioScheduler as Scheduler
from vedro.events import StartupEvent

from ._utils import dispatcher, fire_arg_parsed_event, make_vscenario, tagger

__all__ = ("dispatcher", "tagger")  # fixtures


@pytest.mark.usefixtures(tagger.__name__)
async def test_no_tags(*, dispatcher: Dispatcher):
    with given:
        await fire_arg_parsed_event(dispatcher, tags=None)

        scenarios = [make_vscenario(), make_vscenario()]
        scheduler = Scheduler(scenarios)
        startup_event = StartupEvent(scheduler)

    with when:
        await dispatcher.fire(startup_event)

    with then:
        assert list(scheduler.scheduled) == scenarios


@pytest.mark.usefixtures(tagger.__name__)
async def test_nonexisting_tag(*, dispatcher: Dispatcher):
    with given:
        await fire_arg_parsed_event(dispatcher, tags="SMOKE")

        scenarios = [make_vscenario(), make_vscenario()]
        scheduler = Scheduler(scenarios)
        startup_event = StartupEvent(scheduler)

    with when:
        await dispatcher.fire(startup_event)

    with then:
        assert list(scheduler.scheduled) == []


@pytest.mark.usefixtures(tagger.__name__)
async def test_tag(*, dispatcher: Dispatcher):
    with given:
        await fire_arg_parsed_event(dispatcher, tags="SMOKE")

        scenarios = [
            make_vscenario(tags=["SMOKE"]),
            make_vscenario(),
            make_vscenario(tags=["SMOKE", "P0"])
        ]
        scheduler = Scheduler(scenarios)
        startup_event = StartupEvent(scheduler)

    with when:
        await dispatcher.fire(startup_event)

    with then:
        assert list(scheduler.scheduled) == [scenarios[0], scenarios[2]]


@pytest.mark.usefixtures(tagger.__name__)
async def test_tag_not_operator(*, dispatcher: Dispatcher):
    with given:
        await fire_arg_parsed_event(dispatcher, tags="not SMOKE")

        scenarios = [
            make_vscenario(tags=["SMOKE"]),
            make_vscenario(),
            make_vscenario(tags=["SMOKE", "P0"])
        ]
        scheduler = Scheduler(scenarios)
        startup_event = StartupEvent(scheduler)

    with when:
        await dispatcher.fire(startup_event)

    with then:
        assert list(scheduler.scheduled) == [scenarios[1]]


@pytest.mark.usefixtures(tagger.__name__)
async def test_tag_and_operator(*, dispatcher: Dispatcher):
    with given:
        await fire_arg_parsed_event(dispatcher, tags="SMOKE and P0")

        scenarios = [
            make_vscenario(tags=["SMOKE"]),
            make_vscenario(),
            make_vscenario(tags=["SMOKE", "P0"]),
            make_vscenario(tags=["P0"])
        ]
        scheduler = Scheduler(scenarios)
        startup_event = StartupEvent(scheduler)

    with when:
        await dispatcher.fire(startup_event)

    with then:
        assert list(scheduler.scheduled) == [scenarios[2]]


@pytest.mark.usefixtures(tagger.__name__)
async def test_tag_or_operator(*, dispatcher: Dispatcher):
    with given:
        await fire_arg_parsed_event(dispatcher, tags="SMOKE or P0")

        scenarios = [
            make_vscenario(tags=["SMOKE"]),
            make_vscenario(),
            make_vscenario(tags=["SMOKE", "P0"])
        ]
        scheduler = Scheduler(scenarios)
        startup_event = StartupEvent(scheduler)

    with when:
        await dispatcher.fire(startup_event)

    with then:
        assert list(scheduler.scheduled) == [scenarios[0], scenarios[2]]


@pytest.mark.usefixtures(tagger.__name__)
async def test_tags_expr(*, dispatcher: Dispatcher):
    with given:
        await fire_arg_parsed_event(dispatcher, tags="(not SMOKE) and (not P0)")

        scenarios = [
            make_vscenario(tags=["SMOKE"]),
            make_vscenario(),
            make_vscenario(tags=["SMOKE", "P0"])
        ]
        scheduler = Scheduler(scenarios)
        startup_event = StartupEvent(scheduler)

    with when:
        await dispatcher.fire(startup_event)

    with then:
        assert list(scheduler.scheduled) == [scenarios[1]]


@pytest.mark.usefixtures(tagger.__name__)
async def test_tags_skipped(*, dispatcher: Dispatcher):
    with given:
        await fire_arg_parsed_event(dispatcher, tags="SMOKE")

        scenarios = [
            make_vscenario(tags=["SMOKE"], is_skipped=True),
            make_vscenario(is_skipped=True),
            make_vscenario(),
        ]
        scheduler = Scheduler(scenarios)
        startup_event = StartupEvent(scheduler)

    with when:
        await dispatcher.fire(startup_event)

    with then:
        assert list(scheduler.scheduled) == [scenarios[0]]
