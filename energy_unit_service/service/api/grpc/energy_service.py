import logging
import grpc

import proto.energy_unit.energy_unit_pb2 as pb2
import proto.energy_unit.energy_unit_pb2_grpc as pb2_grpc

from service.domain.magnet_system.inductor import Inductor
from service.domain.cooling.turbine import Turbine
from service.domain import Model

logger = logging.getLogger(__name__)


class EnergyService(pb2_grpc.EnergyUnitServiceServicer):

    def __init__(self, model: Model):
        self.__model = model

    @staticmethod
    def __extract_cell_name(request) -> str:
        return pb2.EnergyCell.Name(request.energy_cell).lower()

    def GetBattery(self, request, context):
        cell_name = EnergyService.__extract_cell_name(request)

        if cell_name not in self.__model.power_cells:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Failed to find cell with name={cell_name}")

            logger.error(
                f"Failed to execute 'GetBattery' rpc due to cell with name={cell_name} doesn't exists!"
            )

            return pb2.Battery()

        power_cell = self.__model.power_cells[cell_name]
        battery = power_cell.battery

        result = {
            "name": battery.name,
            "is_on": battery.is_on,
            "alarm_state": battery.alarm,
            "charge_level": battery.charge_level,
            "capacitors": [
                {
                    "name": capacitor.name,
                    "is_on": capacitor.is_on,
                    "durability": capacitor.durability,
                    "rated_voltage": capacitor.rated_voltage,
                }
                for capacitor in battery.capacitors
            ],
        }

        logger.debug(f"'GetBattery' rpc executed success, response sent!")

        return pb2.Battery(**result)

    def GetCoolingSystem(self, request, context):
        cell_name = EnergyService.__extract_cell_name(request)

        if cell_name not in self.__model.power_cells:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Failed to find cell with name={cell_name}")

            logger.error(
                f"Failed to execute 'GetCoolingSystem' rpc due to cell with name={cell_name} doesn't exists!"
            )

            return pb2.CoolingSystem()

        power_cell = self.__model.power_cells[cell_name]
        cooling_system = power_cell.cooling_system

        def __turbine_serializer(turbine: Turbine):
            return {
                "name": turbine.name,
                "is_on": turbine.is_on,
                "alarm_state": turbine.alarm,
                "durability": turbine.durability,
                "rpm": turbine.rpm,
                "input_current": turbine.input_current,
                "input_voltage": turbine.input_voltage,
                "input_power": turbine.input_power,
            }

        result = {
            "name": cooling_system.name,
            "is_on": cooling_system.is_on,
            "alarm_state": cooling_system.alarm,
            "durability": cooling_system.durability,
            "liquid_cooler": {
                "name": cooling_system.liquid_cooler.name,
                "is_on": cooling_system.liquid_cooler.is_on,
                "alarm_state": cooling_system.liquid_cooler.alarm,
                "durability": cooling_system.liquid_cooler.durability,
                "liquid_storage": {
                    "name": cooling_system.liquid_cooler.liquid_storage.name,
                    "durability": cooling_system.liquid_cooler.liquid_storage.durability,
                    "liquid_level": cooling_system.liquid_cooler.liquid_storage.liquid_level,
                },
                "turbines": [
                    __turbine_serializer(turbine)
                    for turbine in cooling_system.liquid_cooler.turbines
                ],
            },
            "turbines": [
                __turbine_serializer(turbine) for turbine in cooling_system.turbines
            ],
        }

        logger.debug(f"'GetCoolingSystem' rpc executed success, response sent!")

        return pb2.CoolingSystem(**result)

    def GetMagnetSystem(self, request, context):
        cell_name = EnergyService.__extract_cell_name(request)

        if cell_name not in self.__model.power_cells:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Failed to find cell with name={cell_name}")

            logger.error(
                f"Failed to execute 'GetMagnetSystem' rpc due to cell with name={cell_name} doesn't exists!"
            )

            return pb2.MagnetSystem()

        power_cell = self.__model.power_cells[cell_name]
        magnet_system = power_cell.magnet_system

        def __inductor_serializer(inductor: Inductor):
            return {
                "name": inductor.name,
                "is_on": inductor.is_on,
                "durability": inductor.durability,
                "storable_energy": inductor.storable_energy,
                "electromotive_force": inductor.electromotive_force,
                "starter_current": inductor.starter_current,
                "output_current": inductor.output_current,
                "current_loss": inductor.current_loss,
                "q_factor": inductor.q_factor,
            }

        result = {
            "name": magnet_system.name,
            "is_on": magnet_system.is_on,
            "alarm_state": magnet_system.alarm,
            "durability": magnet_system.durability,
            "induction": magnet_system.induction,
            "temperature": magnet_system.temperature,
            "output_current": magnet_system.output_current,
            "voltage": magnet_system.voltage,
            "toroidal_inductors": [
                __inductor_serializer(inductor)
                for inductor in magnet_system.toroidal_inductors
            ],
            "poloidal_inductors": [
                __inductor_serializer(inductor)
                for inductor in magnet_system.poloidal_inductors
            ],
        }

        logger.debug(f"'GetMagnetSystem' rpc executed success, response sent!")

        return pb2.MagnetSystem(**result)

    def GetPlasmaHeater(self, request, context):
        cell_name = EnergyService.__extract_cell_name(request)

        if cell_name not in self.__model.power_cells:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Failed to find cell with name={cell_name}")

            logger.error(
                f"Failed to execute 'GetPlasmaHeater' rpc due to cell with name={cell_name} doesn't exists!"
            )

            return pb2.PlasmaHeater()

        power_cell = self.__model.power_cells[cell_name]
        plasma_heater = power_cell.plasma_heater

        result = {
            "name": plasma_heater.name,
            "is_on": plasma_heater.is_on,
            "alarm_state": plasma_heater.alarm,
            "durability": plasma_heater.durability,
            "temperature": plasma_heater.temperature,
            "output_power_watt": plasma_heater.output_power_watt,
            "input_current": plasma_heater.input_current,
            "input_voltage": plasma_heater.input_voltage,
            "input_power": plasma_heater.input_power,
        }

        logger.debug(f"'GetPlasmaHeater' rpc executed success, response sent!")

        return pb2.PlasmaHeater(**result)

    def GetVacuumVessel(self, request, context):
        cell_name = EnergyService.__extract_cell_name(request)

        if cell_name not in self.__model.power_cells:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Failed to find cell with name={cell_name}")

            logger.error(
                f"Failed to execute 'GetVacuumVessel' rpc due to cell with name={cell_name} doesn't exists!"
            )

            return pb2.VacuumVessel()

        power_cell = self.__model.power_cells[cell_name]
        vacuum_vessel = power_cell.vacuum_vessel

        result = {
            "name": vacuum_vessel.name,
            "is_on": vacuum_vessel.is_on,
            "alarm_state": vacuum_vessel.alarm,
            "durability": vacuum_vessel.durability,
            "pressure": vacuum_vessel.pressure,
            "input_current": vacuum_vessel.input_current,
            "input_voltage": vacuum_vessel.input_voltage,
            "input_power": vacuum_vessel.input_power,
        }

        logger.debug(f"'GetVacuumVessel' rpc executed success, response sent!")

        return pb2.VacuumVessel(**result)
