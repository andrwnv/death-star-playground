class PressureStabilizer:

    def __init__(self, name: str = "pressure_stabilizer") -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.durability = 100.0
        self.time = 0.0
        self.stabilizing_time = 0.0

        self.is_suitable = False

        self.pressure = 750.0
        self.CO2_volume = 1.5
        self.O2_volume = 20.0
        self.N2_volume = 78.0
        self.other_volume = 100-(
            sum([
                self.CO2_volume, 
                self.N2_volume, 
                self.N2_volume
            ])
        )

    def start(self) -> None:
        self.is_on = True

    is_on: bool
    alarm: bool
    durability: float
    repair_time: float
    stabilizing_time: float

    is_suitable: bool

    pressure: float
    CO2_volume: float
    O2_volume: float
    N2_volume: float
    other_volume: float
