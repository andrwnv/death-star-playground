import uuid

from service.domain.battery.battery import Battery
from service.domain.cooling.cooling_system import CoolingSystem
from service.domain.magnet_system.magnet_system import MagnetSystem
from service.domain.plasma_heater.plasma_heater import PlasmaHeater
from service.domain.vacuum_vessel.vacuum_vessel import VacuumVessel
from service.domain.liquid_storage.liquid_storage import (
    LiquidStorage,
)


class PowerCell:

    def __init__(self, name: str = "power_cell") -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.durability = 100.0

        self.cooling_system = CoolingSystem(name=f"CoolingSystem-{uuid.uuid4()}")
        self.magnet_system = MagnetSystem(name=f"MagnetSystem-{uuid.uuid4()}")
        self.plasma_heater = PlasmaHeater(name=f"PlasmaHeater-{uuid.uuid4()}")
        self.vacuum_vessel = VacuumVessel(name=f"VacuumVessel-{uuid.uuid4()}")
        self.fuel_storage = LiquidStorage(name=f"LiquidStorage-{uuid.uuid4()}")
        self.battery = Battery(name=f"Battery-{uuid.uuid4()}")

        self.power = 0.0

    def start(self) -> None:
        self.is_on = True

        self.cooling_system.start()
        self.magnet_system.start()
        self.plasma_heater.start()
        self.vacuum_vessel.start()
        self.battery.start()

    name: str

    is_on: bool
    alarm: bool

    durability: float

    cooling_system: CoolingSystem
    magnet_system: MagnetSystem
    plasma_heater: PlasmaHeater
    vacuum_vessel: VacuumVessel
    fuel_storage: LiquidStorage
    battery: Battery

    power: float
