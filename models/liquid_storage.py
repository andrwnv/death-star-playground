from utils.json_serializable import IJsonSerializable


class LiquidStorage(IJsonSerializable):
    def __init__(self, name: str = 'liquid_storage'):
        self.name = name

        self.durability = 100.0
        self.liquid_level = 100.0

    name: str

    durability: float
    liquid_level: float
