from typing import List
import uuid

from service.domain.models.energy_system.cooling.turbine import Turbine
from service.domain.models.liquid_storage import LiquidStorage

from service.utils.json_serializable import IJsonSerializable


class LiquidCooler(IJsonSerializable):
    def __init__(self, name: str = "liquid_cooler") -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.durability = 100.0

        self.liquid_storage = LiquidStorage(name=f"LiquidStorage-{uuid.uuid4()}")
        self.turbines = []
        for i in range(6):
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
