import abc
import datetime
import logging
from typing import Callable

from death_star.scenarist.abstract_scenario import AbstractAction, AbstractScenario
from death_star.scenarist.event_executor import EventExecutor

logger = logging.getLogger(__name__)


class Scenarist:
    def __init__(self, event_executor: EventExecutor,
                 scenario: AbstractScenario = None, debug_mode: bool = False) -> None:

        self.__event_executor = event_executor
        self._debug_mode = debug_mode

        if scenario:
            self.__active_scenario = scenario

    def set_scenario(self, scenario: AbstractScenario) -> None:
        self.__active_scenario = scenario

    def start(self, async_executor: Callable) -> None:
        if self.__is_running:
            return None

        self.__is_running = True

        if not self.__active_scenario:
            logger.error("Can't run scenarist! No active scenario for run!")
            raise RuntimeError

        if not self.__event_executor.is_running():
            self.__event_executor.start()
            return
        self.__action_executor = async_executor

        async_executor(self.__job)

    def stop(self) -> None:
        self.__is_running = False

    def is_running(self) -> bool:
        return self.__is_running

    def __job(self) -> None:
        from time import sleep

        try:
            while self.__is_running or not self.__active_scenario.is_end():
                action = self.__active_scenario.next_action()

                while action and action.is_extra_action():
                    self.__action_executor(self.__execute_action, args=(action,))
                    action = self.__active_scenario.next_action()

                try:
                    if action:
                        logger.info(f'Start act with name "{action.name()}", with period {action.period()} s.')
                        self.__action_executor(self.__execute_action, args=(action,))
                    else:
                        self.stop()

                    sleep(self.__active_scenario.next_action_period())
                except Exception as ex:
                    logger.error(
                        f"Error while executing scenario action. Exception: {ex}")
        except Exception as ex:
            logger.error(f"Internal error. Exception: {ex}")

    def __execute_action(self, action: AbstractAction) -> None:
        from time import sleep
        if action:
            logger.info(f'Action with name "{action.name()}" start.')

            while not action.is_end():
                action_result = action()
                logger.debug(f'Action {action.name()} was executed with status = {action_result}')
                sleep(action.period())

            logger.info(f'Action {action.name()} end.')
        else:
            logger.error('Action is null, cant start')

    __is_running: bool = False

    __active_scenario: AbstractScenario = None
    __action_executor: Callable = None

    __event_executor: EventExecutor = None

    _begin_timestamp: datetime.time = None
    _debug_mode: bool = False
