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


@dataclass
class ListTeamBoards:
    boards: list[TeamBoard]

    @staticmethod
    def from_dict(obj: Any) -> "ListTeamBoards":
        boards: list[TeamBoard] = [
            team_board_from_dict(item) for item in get_object(obj, "values")
        ]

        return ListTeamBoards(boards)

    def to_dict(self) -> dict:
        result: dict = {}
        result["boards"] = self.boards
        return result


def team_board_from_dict(s: Any) -> TeamBoard:
    return TeamBoard.from_dict(s)


def team_board_to_dict(x: TeamBoard) -> dict:
    return x.to_dict()


def team_board_list_from_dict(s: Any) -> ListTeamBoards:
    return ListTeamBoards.from_dict(s)


def team_board_list_to_dict(x: ListTeamBoards) -> dict:
    return x.to_dict()
