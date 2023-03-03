from datetime import datetime, timedelta
from queue import Queue
import logging

from models.energy_system.battery.battery import Battery
from models.energy_system.plasma_heater.plasma_heater import PlasmaHeater
from models.model import Model

from usecases.abstract_scenario import AbstractAction, AbstractScenario

logger = logging.getLogger(__name__)


class FirstActAction(AbstractAction):
    def __init__(self, name: str, event_executor, model: Model, period: float = 1.0) -> None:
        super().__init__(name)
        self._period = period
        self.__event_executor = event_executor

        self.__start_time = None
        self.__model = model

    def __call__(self) -> bool:
        if not self.__start_time:
            self.__start_time = datetime.now()

        logger.info(f'{self.name()} make tick!')

        for power_cell in self.__model.power_cells.values():
            plasma_heater = power_cell.plasma_heater
            battery = power_cell.battery

            if plasma_heater.durability >= 90.0:
                for capicator in battery.capacitors:
                    if capicator.durability >= 60:
                        if capicator.charge_level + 25 >= 100:
                            capicator.charge_level = 100.0
                            continue
                        capicator.charge_level += 25.0
                        break

    def is_end(self) -> bool:
        if not self.__start_time:
            self.__start_time = datetime.now()
        return (self.__start_time + timedelta(minutes=3)) <= datetime.now()

    def is_extra_action(self) -> bool:
        return False

    def period(self) -> float:
        return 1.0

    __start_time = None


class SecondActAction(AbstractAction):
    def __init__(self, name: str, event_executor, model: Model, period: float = 1.0) -> None:
        super().__init__(name)
        self._period = period
        self.__event_executor = event_executor

        self.__start_time = None
        self.__model = model

    def __call__(self) -> bool:
        if not self.__start_time:
            self.__start_time = datetime.now()

            for power_cell in self.__model.power_cells.values():
                power_cell.plasma_heater.durability = 29.0
                power_cell.plasma_heater.alarm = True

        logger.info(f'{self.name()} make tick!')

        delta_time = (datetime.now() - self.__start_time).seconds
        if delta_time % 60 == 0 and delta_time != 0:
            for power_cell in self.__model.power_cells.values():
                counter = 0
                battery = power_cell.battery
                for capicator in battery.capacitors:
                    if counter == 2:
                        break

                    if capicator.durability > 0:
                        logger.info(f'1 min. end! Break capicators for {power_cell.name}!')
                        capicator.durability = 0
                        
                        counter += 1

        for power_cell in self.__model.power_cells.values():
            plasma_heater = power_cell.plasma_heater
            battery = power_cell.battery

            if plasma_heater.durability <= 29.0:
                if plasma_heater.temperature - 100000 <= 0:
                    plasma_heater.temperature = 0
                else:
                    plasma_heater.temperature -= 100000

                for capicator in battery.capacitors:
                    if capicator.durability < 60:
                        capicator.charge_level = 0
                        continue
                    if capicator.charge_level - 15.0 <= 0:
                        capicator.charge_level = 0
                        continue
                    capicator.charge_level -= 15.0
                    break
            else:
                power_cell.plasma_heater.alarm = False
                if plasma_heater.temperature + 250000 <= 0:
                    plasma_heater.temperature = 11000000
                else:
                    plasma_heater.temperature += 250000
                for capicator in battery.capacitors:
                    if capicator.durability >= 60:
                        if capicator.charge_level + 25 >= 100:
                            capicator.charge_level = 100.0
                            continue
                        capicator.charge_level += 25.0
                        break

    def is_end(self) -> bool:
        if not self.__start_time:
            self.__start_time = datetime.now()

            for power_cell in self.__model.power_cells.values():
                power_cell.plasma_heater.durability = 29.0
                power_cell.plasma_heater.alarm = True

        return (self.__start_time + timedelta(minutes=4)) <= datetime.now()


    def is_extra_action(self) -> bool:
        return False

    def period(self) -> float:
        return 2

    __start_time = None

class ThirdActAction(AbstractAction):
    def __init__(self, name: str, event_executor, model: Model, period: float = 1.0) -> None:
        super().__init__(name)
        self._period = period
        self.__event_executor = event_executor

        self.__start_time = None
        self.__model = model

    def __call__(self) -> bool:
        if not self.__start_time:
            self.__start_time = datetime.now()

            for power_cell in self.__model.power_cells.values():
                power_cell.plasma_heater.durability = 0
                power_cell.plasma_heater.alarm = True
        
        logger.info(f'{self.name()} make tick!')

        delta_time = (datetime.now() - self.__start_time).seconds
        if delta_time % 60 == 0 and delta_time != 0:
            for power_cell in self.__model.power_cells.values():
                counter = 0
                battery = power_cell.battery
                for capicator in battery.capacitors:
                    if counter == 4:
                        break

                    if capicator.durability > 0:
                        logger.info(f'1 min. end! Break capicators for {power_cell.name}!')
                        capicator.durability = 0
                        
                        counter += 1

        for power_cell in self.__model.power_cells.values():
            plasma_heater = power_cell.plasma_heater
            battery = power_cell.battery

            if plasma_heater.durability <= 29.0:
                if plasma_heater.temperature - 100000 <= 0:
                    plasma_heater.temperature = 0
                else:
                    plasma_heater.temperature -= 100000

                for capicator in battery.capacitors:
                    if capicator.durability < 60:
                        capicator.charge_level = 0
                        continue
                    if capicator.charge_level - 15.0 <= 0:
                        capicator.charge_level = 0
                        continue
                    capicator.charge_level -= 15.0
                    break
            else:
                power_cell.plasma_heater.alarm = False
                if plasma_heater.temperature + 250000 <= 0:
                    plasma_heater.temperature = 11000000
                else:
                    plasma_heater.temperature += 250000
                for capicator in battery.capacitors:
                    if capicator.durability >= 60:
                        if capicator.charge_level + 25 >= 100:
                            capicator.charge_level = 100.0
                            continue
                        capicator.charge_level += 25.0
                        break

    def is_end(self) -> bool:
        if not self.__start_time:
            self.__start_time = datetime.now()

            for power_cell in self.__model.power_cells.values():
                power_cell.plasma_heater.durability = 0
                power_cell.plasma_heater.alarm = True

        return (self.__start_time + timedelta(minutes=3)) <= datetime.now()

    def is_extra_action(self) -> bool:
        return False

    def period(self) -> float:
        return 1

    __start_time = None


class BattertScenario(AbstractScenario):
    def __init__(self, model) -> None:
        super().__init__()

        self.__model = model

        self.__period_list = Queue()

        self.__period_list.put_nowait(200)
        self.__period_list.put_nowait(260)
        self.__period_list.put_nowait(30)

    def is_end(self) -> bool:
        return self._action_queue.qsize() == 0

    def is_win(self) -> bool | None:
        is_win = False

        for power_cell in self.__model.power_cells.values():
            battery = power_cell.battery

            fine_capicator_dur_count = 0
            for capicator in battery.capacitors:
                if capicator.durability >= 70 and capicator.charge_level > 0:
                    fine_capicator_dur_count += 1
            if fine_capicator_dur_count >= 40:
                is_win |= True

        return is_win and self.is_end()

    def next_action_period(self) -> float:
        if self.__period_list.qsize() == 0:
            return 0

        return self.__period_list.get_nowait()

    __period_list: Queue[float]
