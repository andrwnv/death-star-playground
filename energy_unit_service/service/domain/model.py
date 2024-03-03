from service.domain.power_cell import PowerCell


class Model:
    def __init__(self) -> None:
        self.power_cells = {
            "alpha_cell": PowerCell("alpha_cell"),
            "theta_cell": PowerCell("theta_cell"),
        }
