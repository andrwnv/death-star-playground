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

    # TODO(andrwnv): add for implemented generators
    # @abstractmethod
    # def go_unstable(self) -> str:
    #     pass
