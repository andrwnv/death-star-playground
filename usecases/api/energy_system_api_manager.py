from copy import copy
from typing import Dict, Optional, List
from models.energy_system.battery.battery import Battery

from models.energy_system.power_cell import PowerCell
from models.energy_system.cooling.cooling_system import CoolingSystem
from models.energy_system.magnet_system.magnet_system import MagnetSystem
from models.energy_system.plasma_heater.plasma_heater import PlasmaHeater
from models.energy_system.vacuum_vessel.vacuum_vessel import VacuumVessel
from models.liquid_storage import LiquidStorage


class EnergySystemApiManager:
    def __init__(self, power_cells: Dict[str, PowerCell]) -> None:
        self.__power_cells = power_cells

    def get_list(self) -> List[str]:
        return list(self.__power_cells.keys())

    def get_state(self, name: str) -> PowerCell:
        cell = self.__power_cells[name]
        cell.power = 104.0 - \
            4.0 ** ((11.0 * float(10 ** 6) - float(cell.plasma_heater.temperature)) / 10.0 ** 6)
        return copy(cell)

    def get_colling_system_state(self, name: str) -> Optional[CoolingSystem]:
        if name not in self.__power_cells:
            return None
        return copy(self.__power_cells[name].cooling_system)

    def get_magnet_system_state(self, name: str) -> Optional[MagnetSystem]:
        if name not in self.__power_cells:
            return None
        return copy(self.__power_cells[name].magnet_system)

    def get_plasma_heater_state(self, name: str) -> Optional[PlasmaHeater]:
        if name not in self.__power_cells:
            return None
        return copy(self.__power_cells[name].plasma_heater)

    def get_vacuum_vessel_state(self, name: str) -> Optional[VacuumVessel]:
        if name not in self.__power_cells:
            return None
        return copy(self.__power_cells[name].vacuum_vessel)

    def get_fuel_storage_state(self, name: str) -> Optional[LiquidStorage]:
        if name not in self.__power_cells:
            return None
        return copy(self.__power_cells[name].fuel_storage)

    def get_battery_state(self, name: str) -> Optional[Battery]:
        if name not in self.__power_cells:
            return None
        return copy(self.__power_cells[name].battery)

    __power_cells: Dict[str, PowerCell]
