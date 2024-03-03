class HumidityController:
    def __init__(self, name: str = "CGH-C8C7") -> None:
        self.name = name

        self.is_on = False
        self.durability = 100.0
        self.time_before_stabilize_ms = 0
        self.current_humidity = 0
