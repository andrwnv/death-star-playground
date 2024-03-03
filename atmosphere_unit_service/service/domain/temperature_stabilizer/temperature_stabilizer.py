class TemperatureStabilizer:

    def __init__(self, name: str = "temperature_stabilizer") -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.durability = 100.0

        self.temperature = 24.0
        self.sun_side = False

    def start(self) -> None:
        self.is_on = True
    
    is_on: bool
    alarm: bool
    durability: float

    temperature: float
    sun_side: bool
