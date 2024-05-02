from dataclasses import dataclass
from typing import Any

from utilities.utils import get_object


@dataclass
class TeamBoard:
    team_board_id: int
    name: str
    team_board_type: str

    @staticmethod
    def from_dict(obj: Any) -> "TeamBoard":
        team_board_id: int = int(get_object(obj, "id"))
        name: str = get_object(obj, "name")
        team_board_type: str = get_object(obj, "type")

        return TeamBoard(team_board_id, name, team_board_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["team_board_id"] = int(self.team_board_id)
        result["name"] = self.name
        result["team_board_type"] = self.team_board_type
        return result
