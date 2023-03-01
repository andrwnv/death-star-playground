from pydantic import BaseModel


class SendTeamDto(BaseModel):
    team_name: str
    cell_name: str
    location: str
