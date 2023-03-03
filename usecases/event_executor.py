import copy
import uuid
import logging
import abc

from typing import Callable, Dict, List

from usecases.abstract_event import AbstractEvent
from usecases.test_event import TestEvent
from utils.timer import NonBlockableTimer

logger = logging.getLogger(__name__)


class IEventExecutorManager(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def active_events(self) -> List[AbstractEvent]:
        raise NotImplementedError


class EventExecutor(IEventExecutorManager):
    def __init__(self, interval: float, async_executor: Callable, debug_mode: bool = False) -> None:
        self.__debug_mode = debug_mode
        self.__interval = interval

        self.__is_running = False
        self.__events = {}
        self.__ready_to_execute_events = []

        self.__timer = NonBlockableTimer(
            self.__interval, async_executor=async_executor, callback=self.__job)

    def start(self, on_event_execute_handler: Callable[[AbstractEvent], None]) -> None:
        self.__timer.start()
        self.__is_running = True
        self.__on_event_execute_handler = on_event_execute_handler

    def stop(self) -> None:
        self.__timer.stop()
        self.__is_running = False
        self.__on_event_execute_handler = None

    def is_running(self) -> bool:
        return self.__is_running

    def active_events(self) -> List[AbstractEvent]:
        return list(self.__events.values())

    def push_event(self, event: AbstractEvent) -> None:
        if not event:
            logger.warning(f"Unsuccessful push none {event.name()} event!")
            return

        self.__events[uuid.uuid4()] = event

    def __job(self) -> None:
        try:
            self.__prepare_ready_events()
            if len(self.__ready_to_execute_events) > 0:
                try:
                    event = self.__ready_to_execute_events.pop()
                    self.__on_event_execute_handler(copy.copy(event))
                    self.__execute_event(event)
                except Exception as ex:
                    logger.warning(
                        f"Error while executing event. Exception: {ex}")
        except Exception as ex:
            logger.error(f"Internal error. Exception: {ex}")

    def __execute_event(self, event: AbstractEvent) -> bool:
        if not event:
            logger.warning(
                f"Unsuccessful execution of NULL {event.name()} event!")
            return False

        try:
            if not self.__debug_mode:
                event.negative_effect()
            event.positive_effect()
            return True
        except Exception as ex:
            logger.error(
                f"Error while execute {event.name()} event effects. Exception: {ex}")
            return False

    def __prepare_ready_events(self) -> None:
        for key, event in list(self.__events.items()):
            if self.__debug_mode:
                logger.debug(
                    f"{key}: Event {event.name()} time to execution = {event.is_soon()}")

            if event.is_ready():
                self.__ready_to_execute_events.append(
                    self.__events.pop(key))

    __debug_mode: bool

    __is_running: bool
    __interval: float

    __events: Dict[uuid.UUID, AbstractEvent]
    __ready_to_execute_events: List[AbstractEvent]

    __timer: NonBlockableTimer = None
