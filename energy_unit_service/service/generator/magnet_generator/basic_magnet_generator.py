from dataclasses import dataclass
from typing import List
import random

import uuid

from service.domain.magnet_system.inductor import Inductor
from service.domain.magnet_system.magnet_system import MagnetSystem
from service.generator.generation_strategy import (
    IGenerationStrategy,
)


class DefaultGenerationStrategy(IGenerationStrategy):
    @dataclass
    class GenerationParams:
        # Inductor
        OUTPUT_CURRENT = 275.0
        CURRENT_LOSS = 26.6

        # MagnetSystem
        TEMPERATURE = 120.5
        INDUCTION = 13

        SIGMA = 14.0
        INDUCTION_SIGMA = 1.04567523154

    def __init__(
        self,
        model: MagnetSystem,
        name: str = f"MagnetSystemDefaultGenerator-{uuid.uuid4()}",
    ) -> None:
        super().__init__()

        self.__model = model
        self.__name = name

    def generate_properties(self) -> None:
        def __inductor_params_generator(inductors: List[Inductor]):
            for inductor in inductors:
                if inductor.is_on:
                    inductor.output_current = random.gauss(
                        self.GenerationParams.OUTPUT_CURRENT,
                        self.GenerationParams.SIGMA,
                    )
                    inductor.current_loss = random.gauss(
                        self.GenerationParams.CURRENT_LOSS, self.GenerationParams.SIGMA
                    )

                    inductor.electromotive_force = (
                        inductor.output_current / inductor.current_loss
                    )
                    inductor.q_factor = (
                        inductor.output_current / inductor.starter_current
                    )

        if not self.__model.is_on:
            pass

        self.__model.alarm = False

        __inductor_params_generator(self.__model.toroidal_inductors)
        __inductor_params_generator(self.__model.poloidal_inductors)

        self.__model.temperature = random.gauss(
            self.GenerationParams.TEMPERATURE, self.GenerationParams.SIGMA
        )

        self.__model.output_current += sum(
            inductor.output_current - inductor.current_loss
            for inductor in self.__model.toroidal_inductors
        )
        self.__model.output_current += sum(
            inductor.output_current - inductor.current_loss
            for inductor in self.__model.poloidal_inductors
        )

        self.__model.induction = random.gauss(
            self.GenerationParams.INDUCTION, self.GenerationParams.INDUCTION_SIGMA
        )

        self.__model.voltage = self.__model.output_current / 526.0

        if self.__model.durability <= 70:
            self.__model.alarm = True

    def name(self) -> str:
        return self.__name

    __model: MagnetSystem = None
    __name: str = ""
