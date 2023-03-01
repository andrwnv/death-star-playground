from models.energy_system.battery.battery import Battery
from usecases.abstract_scenario import AbstractAction

from random import randrange


class DebugBreakAction(AbstractAction):
    def __init__(self, name: str, battery: Battery, is_extra: bool = False, period: float = 2.0) -> None:
        super().__init__(name)
        self.__is_extra = is_extra
        self._period = period
        self.__battery = battery

    def __call__(self) -> bool:
        for _ in range(5):
            capacitor_ix = randrange(len(self.__battery.capacitors))

            if self.__battery.capacitors[capacitor_ix].durability >= 50:
                self.__battery.capacitors[capacitor_ix].durability -= 4.256
        
        return True

    def is_end(self) -> bool:
        self.__counter += 1
        return self.__counter > 3

    def is_extra_action(self) -> bool:
        return self.__is_extra

    __is_extra: bool
    __counter = 0
    __battery: Battery = None
