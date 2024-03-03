from typing import Dict

from service.domain.models.energy_system.power_cell import PowerCell
from service.domain.models.repair_team.team import RepairTeam


class Model:
    def __init__(self):
        self.power_cells = {"alpha_cell": PowerCell(), "theta_cell": PowerCell()}

        self.repair_teams = {
            "alpha_team": RepairTeam(name="alpha_team"),
            "beta_team": RepairTeam(name="beta_team"),
            "gamma_team": RepairTeam(name="gamma_team"),
            "delta_team": RepairTeam(name="delta_team"),
            "epsilon_team": RepairTeam(name="epsilon_team"),
        }

    def start(self) -> None:
        for cell in self.power_cells.values():
            cell.start()

    power_cells: Dict[str, PowerCell]
    repair_teams: Dict[str, RepairTeam]
