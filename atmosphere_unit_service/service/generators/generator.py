import logging

from dataclasses import dataclass

from service.domain.model import Model

import service.generators.humidity_manager.humidity_manager_generator as humidity_generator
import service.generators.pressure_stabilizer.pressure_stabilizer_generator as pressure_generator
import service.generators.temperature_stabilizer.temperature_stabilizer_generator as temperature_generator

from service.generators.generation_strategy import IGenerationStrategy

logger = logging.getLogger(__name__)

class DomainGenerator:
    @dataclass
    class GeneratorPack:
        humidity_manager_generator: IGenerationStrategy
        pressure_stabilizer_generator: IGenerationStrategy
        temperature_stabilizer_generator: IGenerationStrategy
    
    def __init__(self, model: Model) -> None:
        self.__generator = {}

        for device_sector, device in model.device.items():
            self.__generator[device_sector] = DomainGenerator.GeneratorPack(
                humidity_manager_generator=humidity_generator.DefaultGenerationStrategy(
                    device.humidity_manager
                ),
                pressure_stabilizer_generator=pressure_generator.DefaultGenerationStrategy(
                    device.pressure_stabilizer
                ),
                temperature_stabilizer_generator=temperature_generator.DefaultGenerationStrategy(
                    device.temperature_stabilizer
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
                    generator.humidity_manager_generator.generate_properties()
                    generator.pressure_stabilizer_generator.generate_properties()
                    generator.temperature_stabilizer_generator.generate_properties()

                    logger.debug(
                        f"Generator '{generator_name} generate model properties.'"
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
    