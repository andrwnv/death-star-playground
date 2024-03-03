import logging

from dataclasses import dataclass

from service.domain import Model

import service.generator.battery_generator as battery_generator
import service.generator.cooling_generator as cooling_generator
import service.generator.magnet_generator as magnet_generator
import service.generator.plasma_heater_generator as plasma_heater_generator
import service.generator.vacuum_vessel_generator as vacuum_vessel_generator

from service.generator.generation_strategy import IGenerationStrategy

logger = logging.getLogger(__name__)


class DomainGenerator:
    @dataclass
    class GeneratorPack:
        battery_generator: IGenerationStrategy
        cooling_generator: IGenerationStrategy
        magnet_generator: IGenerationStrategy
        plasma_heater_generator: IGenerationStrategy
        vacuum_vessel_generator: IGenerationStrategy

    def __init__(self, model: Model) -> None:
        self.__generator = {}

        for power_cell_name, power_cell in model.power_cells.items():
            self.__generator[power_cell_name] = DomainGenerator.GeneratorPack(
                battery_generator=battery_generator.DefaultGenerationStrategy(
                    power_cell.battery
                ),
                cooling_generator=cooling_generator.DefaultGenerationStrategy(
                    power_cell.cooling_system
                ),
                magnet_generator=magnet_generator.DefaultGenerationStrategy(
                    power_cell.magnet_system
                ),
                plasma_heater_generator=plasma_heater_generator.DefaultGenerationStrategy(
                    power_cell.plasma_heater
                ),
                vacuum_vessel_generator=vacuum_vessel_generator.DefaultGenerationStrategy(
                    power_cell.vacuum_vessel
                ),
            )

        self.__is_started = False
        self.__generation_interval = 1

    async def run(self):
        import asyncio

        self.__is_started = True

        while self.__is_started:
            for generator_name, generator in self.__generator.items():
                try:
                    generator.battery_generator.generate_properties()
                    generator.cooling_generator.generate_properties()
                    generator.magnet_generator.generate_properties()
                    generator.plasma_heater_generator.generate_properties()
                    generator.vacuum_vessel_generator.generate_properties()

                    logger.debug(
                        f"Generator '{generator_name}' generate model properties."
                    )
                except Exception:
                    logger.error(f"Failed generate properties due to internal error!")

            logger.info(
                f"Model properties was generated success! See you after {self.__generation_interval} sec."
            )

            await asyncio.sleep(self.__generation_interval)

    def stop(self):
        self.__is_started = False

    def set_generation_interval(self, interval: int):
        self.__generation_interval = interval
