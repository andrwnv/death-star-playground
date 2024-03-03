from typing import List

import uuid

from service.domain.cooling.turbine import Turbine
from service.domain.liquid_storage.liquid_storage import (
    LiquidStorage,
)


class LiquidCooler:
    def __init__(self, name: str = "liquid_cooler") -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.durability = 100.0

        self.liquid_storage = LiquidStorage(name=f"LiquidStorage-{uuid.uuid4()}")
        self.turbines = []
        for _ in range(6):
            self.turbines.append(Turbine(name=f"Turbine-{uuid.uuid4()}"))

    def start(self) -> None:
        self.is_on = True
        for turbine in self.turbines:
            turbine.start()

    is_on: bool
    alarm: bool

    durability: float

    liquid_storage: LiquidStorage
    turbines: List[Turbine]
