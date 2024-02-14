from typing import List

import uuid

from service.domain.cooling.liquid_cooler import LiquidCooler
from service.domain.cooling.turbine import Turbine


class CoolingSystem:

    def __init__(self, name: str = "cooling_system") -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.durability = 100.0

        self.turbines = []
        for _ in range(6):
            self.turbines.append(Turbine(name=f"Turbine-{uuid.uuid4()}"))

        self.liquid_cooler = LiquidCooler(name=f"LiquidCooler-{uuid.uuid4()}")

    def start(self) -> None:
        self.is_on = True

        for turbine in self.turbines:
            turbine.start()
        self.liquid_cooler.start()

    is_on: bool
    alarm: bool

    durability: float

    turbines: List[Turbine]
    liquid_cooler: LiquidCooler