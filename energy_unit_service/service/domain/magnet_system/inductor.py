class Inductor:

    def __init__(self, name: str = "inductor") -> None:
        self.name = name

        self.is_on = False
        self.durability = 100.0

        self.storable_energy = 4750.0
        self.electromotive_force = 0.0
        self.starter_current = 201.56
        self.output_current = 0.0
        self.current_loss = 0.0
        self.q_factor = 0.0

    def start(self) -> None:
        self.is_on = True

    is_on: bool

    durability: float

    storable_energy: float
    electromotive_force: float

    starter_current: float
    output_current: float
    current_loss: float

    q_factor: float
