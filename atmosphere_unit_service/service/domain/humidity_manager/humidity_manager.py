class HumidityManager:

    def __init__(self, name: str = "humidity_manager") -> None:
        self.name = name

        self.is_on = False
        self.alarm = False
        self.durability = 100.0

        self.humidity = 60.0

    def start(self) -> None:
        self.is_on = True

    is_on: bool
    alarm: bool
    durability: float

    humidity: float
    