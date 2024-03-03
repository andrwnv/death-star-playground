class PressureBalancer:
    def __init__(self, name: str = "PressureBalancer") -> None:
        self.name = name

        self.is_on = False
        self.overall_durability = 100.0
        self.bb_e8e3_is_on = True
        self.bt_0010_is_on = True
