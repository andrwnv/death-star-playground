import logging
import grpc

import proto.atmosphere_unit.atmosphere_unit_pb2 as pb2
import proto.atmosphere_unit.atmosphere_unit_pb2_grpc as pb2_grpc

from service.domain.device import Device
from service.domain.model import Model

logger = logging.getLogger(__name__)


class AtmosphereService(pb2_grpc.AtmosphereUnitServiceServicer):

    def __init__(self, model: Model):
        self.__model = model

    @staticmethod
    def __extract_device_name(request) -> str:
        return pb2.Device.Name(request.device).lower()

    def GetHumidityManager(self, request, context):
        device_name = AtmosphereService.__extract_device_name(request)

        if device_name not in self.__model.devices:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Failed to find device with name={device_name}")

            logger.error(
                f"Failed to execute 'GetHumidityManager' rpc due to device with name={device_name} doesn't exists!"
            )

            return pb2.HumidityManager()

        device = self.__model.devices[device_name]
        humidity_manager = device.humidity_manager

        result = {
            "name": humidity_manager.name,
            "is_on": humidity_manager.is_on,
            "durability": humidity_manager.durability,
            "humidity": humidity_manager.humidity,
        }

        logger.debug(f"'GetHumidityManager' rpc executed success, response sent!")

        return pb2.HumidityManager(**result)

    def GetPressureStabilizer(self, request, context):
        device_name = AtmosphereService.__extract_device_name(request)

        if device_name not in self.__model.devices:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Failed to find device with name={device_name}")

            logger.error(
                f"Failed to execute 'GetPressureStabilizer' rpc due to device with name={device_name} doesn't exists!"
            )

            return pb2.PressureStabilizer()

        device = self.__model.devices[device_name]
        pressure_stabilizer = device.pressure_stabilizer

        result = {
            "name": pressure_stabilizer.name,
            "is_on": pressure_stabilizer.is_on,
            "durability": pressure_stabilizer.durability,
            "is_suitable": pressure_stabilizer.is_suitable,
            "pressure": pressure_stabilizer.pressure,
            "CO2_volume": pressure_stabilizer.CO2_volume,
            "O2_volume": pressure_stabilizer.O2_volume,
            "N2_volume": pressure_stabilizer.N2_volume,
            "other_volume": pressure_stabilizer.other.volume,
        }

        logger.debug(f"'GetPressureStabilizer' rpc executed success, response sent!")

        return pb2.PressureStabilizer(**result)

    def GetTemperatureStabilizer(self, request, context):
        device_name = AtmosphereService.__extract_device_name(request)

        if device_name not in self.__model.devices:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Failed to find device with name={device_name}")

            logger.error(
                f"Failed to execute 'GetTemperatureStabilizer' rpc due to device with name={device_name} doesn't exists!"
            )

            return pb2.TemperatureStabilizer()

        device = self.__model.devices[device_name]
        temperature_stabilizer = device.temperature_stabilizer

        result = {
            "name": temperature_stabilizer.name,
            "is_on": temperature_stabilizer.is_on,
            "durability": temperature_stabilizer.durability,
            "temperature": temperature_stabilizer.induction,
        }

        logger.debug(f"'GetTemperatureStabilizer' rpc executed success, response sent!")

        return pb2.TemperatureStabilizer(**result)

