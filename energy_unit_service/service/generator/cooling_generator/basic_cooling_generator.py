from dataclasses import dataclass
from typing import List
import random

import uuid

from service.domain.cooling.cooling_system import CoolingSystem
from service.domain.cooling.turbine import Turbine
from service.generator.generation_strategy import (
    IGenerationStrategy,
)


class DefaultGenerationStrategy(IGenerationStrategy):
    @dataclass
    class GenerationParams:
        INPUT_CURRENT = 107.0
        INPUT_POWER = 224.0
        INPUT_VOLTAGE = 275.0
        RPM = 5000.0
        LIQUID_LEVEL = 2000.0

        SIGMA = 14.0

    def __init__(
        self,
        model: CoolingSystem,
        name: str = f"CoolingSystemDefaultGenerator-{uuid.uuid4()}",
    ) -> None:
        super().__init__()

        self.__model = model
        self.__name = name

    def generate_properties(self) -> None:
        def __turbine_params_generator(turbines: List[Turbine]):
            for turbine in turbines:
                turbine.alarm = False

                if turbine.is_on:
                    turbine.input_current = random.gauss(
                        self.GenerationParams.INPUT_CURRENT, self.GenerationParams.SIGMA
                    )
                    turbine.input_power = random.gauss(
                        self.GenerationParams.INPUT_POWER, self.GenerationParams.SIGMA
                    )
                    turbine.input_voltage = random.gauss(
                        self.GenerationParams.INPUT_VOLTAGE, self.GenerationParams.SIGMA
                    )
                    turbine.rpm = random.gauss(
                        self.GenerationParams.RPM, self.GenerationParams.SIGMA
                    )

        if not self.__model.is_on:
            pass

        self.__model.alarm = False
        __turbine_params_generator(self.__model.turbines)

        self.__model.liquid_cooler.alarm = False
        if self.__model.liquid_cooler.is_on:
            __turbine_params_generator(self.__model.liquid_cooler.turbines)
            self.__model.liquid_cooler.liquid_storage.liquid_level = random.gauss(
                self.GenerationParams.LIQUID_LEVEL, 1.0
            )

    def name(self) -> str:
        return self.__name

    __model: CoolingSystem = None
    __name: str = ""
