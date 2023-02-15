from utils.json_serializable import IJsonSerializable


class Capacitor(IJsonSerializable):
    def __init__(self, name: str = 'capacitor') -> None:
        self.name = name

        self.is_on = False
        self.durability = 100.0

        self.charge_level = 100.0
        self.rated_voltage = 0.0
    
    def start(self) -> None:
        self.is_on = True
    
    is_on: bool

    durability: float
    rated_voltage: float
