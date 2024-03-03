from abc import ABC, abstractmethod

from atmosphere_unit_service.service.generators.generation_strategy import IGenerationStrategy

class IGenerator(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def start(self, interval: float) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def is_started(sellf) -> bool:
        pass

    @abstractmethod
    def push_strategy(self, strategy: IGenerationStrategy) -> None:
        pass

    @abstractmethod
    def delete_strategy(self, model_name: str) -> None:
        pass
