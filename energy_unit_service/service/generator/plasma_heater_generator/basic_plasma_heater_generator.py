from dataclasses import dataclass
import random

import uuid

from service.domain.plasma_heater.plasma_heater import PlasmaHeater
from service.generator.generation_strategy import (
    IGenerationStrategy,
)


class DefaultGenerationStrategy(IGenerationStrategy):
    @dataclass
    class GenerationParams:
        TEMPERATURE = 12000000
        OUTPUT_POWER = 124.0
        INPUT_CURRENT = 560.0
        INPUT_VOLTAGE = 340.0
        INPUT_POWER = 700.0

        SIGMA = 14.0
        TEMPERATURE_SIGMA = 750000

    def __init__(
        self,
        model: PlasmaHeater,
        name: str = f"PlasmaHeaterDefaultGenerator-{uuid.uuid4()}",
    ) -> None:
        super().__init__()

        self.__model = model
        self.__name = name

    def generate_properties(self) -> None:
        if not self.__model.is_on:
            pass

        self.__model.alarm = False

        temperature = random.gauss(
            self.GenerationParams.TEMPERATURE, self.GenerationParams.TEMPERATURE_SIGMA
        )

        self.__model.temperature = (
            temperature
            if temperature < self.GenerationParams.TEMPERATURE
            else self.GenerationParams.TEMPERATURE
        )

        self.__model.output_power_watt = random.gauss(
            self.GenerationParams.OUTPUT_POWER, self.GenerationParams.SIGMA
        )
        self.__model.input_current = random.gauss(
            self.GenerationParams.INPUT_CURRENT, self.GenerationParams.SIGMA
        )
        self.__model.input_voltage = random.gauss(
            self.GenerationParams.INPUT_VOLTAGE, self.GenerationParams.SIGMA
        )
        self.__model.input_power = random.gauss(
            self.GenerationParams.INPUT_POWER, self.GenerationParams.SIGMA
        )

        if self.__model.durability <= 30:
            self.__model.alarm = True

    def name(self) -> str:
        return self.__name

    __model: PlasmaHeater = None
    __name: str = ""
