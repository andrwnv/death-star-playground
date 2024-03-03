from typing import List
import uuid

from service.domain.models.energy_system.magnet_system.inductor import Inductor

from service.utils.json_serializable import IJsonSerializable


class MagnetSystem(IJsonSerializable):
    def __init__(self, name: str = "magnet_system") -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.durability = 100.0
        self.induction = 0.0
        self.temperature = 0.0
        self.output_current = 0.0
        self.voltage = 0.0

        self.toroidal_inductors = []
        for i in range(18):
            self.toroidal_inductors.append(
                Inductor(name=f"ToroidalInductor-{uuid.uuid4()}")
            )

        self.poloidal_inductors = []
        for i in range(6):
            self.poloidal_inductors.append(
                Inductor(name=f"PoloidalInductor-{uuid.uuid4()}")
            )

    def start(self) -> None:
        self.is_on = True

        for inductor in self.toroidal_inductors:
            inductor.start()

        for inductor in self.poloidal_inductors:
            inductor.start()

    is_on: bool
    alarm: bool

    durability: float

    induction: float
    temperature: float

    output_current: float
    voltage: float

    toroidal_inductors: List[Inductor]
    poloidal_inductors: List[Inductor]
