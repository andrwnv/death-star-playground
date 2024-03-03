from service.domain.pressure_stabilizer.pressure_stabilizer import PressureStabilizer
from service.domain.temperature_stabilizer.temperature_stabilizer import TemperatureStabilizer
from service.domain.humidity_manager.humidity_manager import HumidityManager

import uuid

class Device:

    def __init__(self, name: str = "device") -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.durability = 100.0

        self.pressure_stabilizer = PressureStabilizer(name=f"PressureStabilizer-{uuid.uuid4()}")
        self.temperature_stabilizer = TemperatureStabilizer(name=f"TemperatureStabilizer-{uuid.uuid4()}")
        self.humidity_manager = HumidityManager(name=f"HumidityManager-{uuid.uuid4}")
    
    def start(self) -> None:
        self.is_on = self.pressure_stabilizer.is_on or \
        self.temperature_stabilizer.is_on or \
        self.humidity_manager.is_on

    is_on: bool
    alarm: bool
    durability: float

    sector: str
