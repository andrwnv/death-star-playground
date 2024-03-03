from abc import ABC, abstractmethod

class IGenerationStrategy(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def generate_properties(self) -> None:
        pass

    @abstractmethod
    def name(self) -> str:
        pass
