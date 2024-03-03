from dataclasses import dataclass
import random

import uuid

from service.domain.vacuum_vessel.vacuum_vessel import VacuumVessel
from service.generator.generation_strategy import (
    IGenerationStrategy,
)


class DefaultGenerationStrategy(IGenerationStrategy):
    @dataclass
    class GenerationParams:
        INPUT_CURRENT = 107.0
        INPUT_POWER = 224.0
        INPUT_VOLTAGE = 275.0
        PRESSURE = 0.145685

        SIGMA = 14.0
        PRESSURE_SIGMA = 0.0354754565241

    def __init__(
        self,
        model: VacuumVessel,
        name: str = f"VacuumVesselDefaultGenerator-{uuid.uuid4()}",
    ) -> None:
        super().__init__()

        self.__model = model
        self.__name = name

    def generate_properties(self) -> None:
        if not self.__model.is_on:
            pass

        self.__model.alarm = False
        self.__model.input_current = random.gauss(
            self.GenerationParams.INPUT_CURRENT, self.GenerationParams.SIGMA
        )
        self.__model.input_power = random.gauss(
            self.GenerationParams.INPUT_POWER, self.GenerationParams.SIGMA
        )
        self.__model.input_voltage = random.gauss(
            self.GenerationParams.INPUT_VOLTAGE, self.GenerationParams.SIGMA
        )
        self.__model.pressure = random.gauss(
            self.GenerationParams.PRESSURE, self.GenerationParams.PRESSURE_SIGMA
        )

    def name(self) -> str:
        return self.__name

    __model: VacuumVessel = None
    __name: str = ""
