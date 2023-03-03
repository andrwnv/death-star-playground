from typing import List
import uuid

from models.energy_system.battery.capacitor import Capacitor

from utils.json_serializable import IJsonSerializable


class Battery(IJsonSerializable):
    def __init__(self, name: str = 'battery') -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.charge_level = 100.0

        self.capacitors = []
        for i in range(65):
            self.capacitors.append(Capacitor(name=f'Capacitor-{uuid.uuid4()}'))

        for i in range(20):
            self.capacitors[i].durability = 100.0

    def start(self) -> None:
        self.is_on = True

        for capacitor in self.capacitors:
            capacitor.start()

    is_on: bool
    alarm: bool

    charge_level: float

    capacitors: List[Capacitor]
