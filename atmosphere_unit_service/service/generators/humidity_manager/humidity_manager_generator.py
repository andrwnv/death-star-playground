from dataclasses import dataclass
from typing import List
import random

import uuid

from service.domain.humidity_manager.humidity_manager import HumidityManager
from service.generators.generation_strategy import (
    IGenerationStrategy,
)

class DefaultGenerationStrategy(IGenerationStrategy):
    @dataclass
    class GenerationParams:
        HUMIDITY = 60.0
        CHANCE = 50.0

        SIGMA = 10.0
    
    def __init__(
        self,
        model: HumidityManager,
        name: str = f"HumidityManagerDefaultGenerator-{uuid.uuid4()}",
    ) -> None:
        super().__init__()

        self.__model = model
        self.__name = name

    def generate_properties(self) -> None:
        if self.__model.is_on:
                self.__model.humidity = random.gauss(
                    self.GenerationParams.HUMIDITY,
                    self.GenerationParams.SIGMA,
                )

        self.__model.alarm = self.__model.durability <= 27

        if self.__model.humidity < 50:
            self.GenerationParams.CHANCE = 50 - self.__model.humidity
            if random(0,100,1) <= self.GenerationParams.CHANCE:
                self.__model.durability -= 1
        
        if self.__model.humidity > 70:
            self.GenerationParams.CHANCE = self.__model.humidity - 70
            if random(0,100,1) <= self.GenerationParams.CHANCE:
                self.__model.durability -= 5

    def name(self) -> str:
        return self.__name

    __model: HumidityManager = None
    __name: str = ""
