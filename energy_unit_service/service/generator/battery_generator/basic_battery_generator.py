from dataclasses import dataclass
from typing import List
import random

import uuid

from service.domain.battery.battery import Battery
from service.domain.battery.capacitor import Capacitor
from service.generator.generation_strategy import (
    IGenerationStrategy,
)


class DefaultGenerationStrategy(IGenerationStrategy):
    @dataclass
    class GenerationParams:
        CHARGE_LEVEL = 100.0
        RATED_VOLTAGE = 124.6

        SIGMA = 14.0

    def __init__(
        self,
        model: Battery,
        name: str = f"BatterySystemDefaultGenerator-{uuid.uuid4()}",
    ) -> None:
        super().__init__()

        self.__model = model
        self.__name = name

    def generate_properties(self) -> None:
        def __capacitor_params_generator(capacitors: List[Capacitor]):
            for capacitor in capacitors:
                if capacitor.is_on:
                    charge_level = random.gauss(
                        self.GenerationParams.CHARGE_LEVEL, self.GenerationParams.SIGMA
                    )

                    if charge_level >= 100.0:
                        charge_level = 100.0
                    capacitor.charge_level = charge_level
                    capacitor.rated_voltage = random.gauss(
                        self.GenerationParams.RATED_VOLTAGE, self.GenerationParams.SIGMA
                    )

        if not self.__model.is_on:
            pass

        self.__model.alarm = False

        __capacitor_params_generator(self.__model.capacitors)

        self.__model.charge_level = sum(
            capicator.charge_level for capicator in self.__model.capacitors
        ) / len(self.__model.capacitors)

    def name(self) -> str:
        return self.__name

    __model: Battery = None
    __name: str = ""
