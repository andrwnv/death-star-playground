class AtmosphereState:
    def __init__(self) -> None:
        self.co2_volume = 0.0
        self.o2_volume = 0.0
        self.n2_volume = 0.0
        self.another_volume = 0.0


class PressureStabilizer:
    def __init__(self, name: str = "BB-E8E3") -> None:
        self.name = name

        self.is_on = False
        self.durability = 100.0

        self.pressure_is_fine = True
        self.time_before_stabilize_ms = 0
        self.current_pressure_mmhg = 0

        self.atmosphere_state = AtmosphereState()
