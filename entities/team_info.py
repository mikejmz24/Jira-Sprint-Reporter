from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from utilities.utils import get_object, get_optional_datetime, get_optional_object


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


@dataclass
class TeamSprint:
    sprint_id: int
    name: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    origin_board_id: int
    goal: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> "TeamSprint":
        sprint_id: int = int(get_object(obj, "id"))
        name: str = get_object(obj, "name")
        start_date: Optional[datetime] = get_optional_datetime(
            obj, "startDate", str_len=-10
        )
        end_date: Optional[datetime] = get_optional_datetime(
            obj, "endDate", str_len=-10
        )
        origin_board_id: int = int(get_object(obj, "originBoardId"))
        goal: Optional[str] = get_optional_object(obj, "goal")
        return TeamSprint(sprint_id, name, start_date, end_date, origin_board_id, goal)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sprint_id"] = int(self.sprint_id)
        result["name"] = self.name
        result["start_date"] = str(self.start_date)
        result["end_date"] = str(self.end_date)
        result["origin_board_id"] = self.origin_board_id
        result["goal"] = self.goal
        return result


@dataclass
class ListTeamSprints:
    sprints: list[TeamSprint]

    @staticmethod
    def from_dict(obj: Any) -> "ListTeamSprints":
        sprints: list[TeamSprint] = [
            team_sprint_from_dict(item) for item in get_object(obj, "values")
        ]
        return ListTeamSprints(sprints)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sprints"] = self.sprints
        return result


def team_board_from_dict(s: Any) -> TeamBoard:
    return TeamBoard.from_dict(s)


def team_board_to_dict(x: TeamBoard) -> dict:
    return x.to_dict()


def team_board_list_from_dict(s: Any) -> ListTeamBoards:
    return ListTeamBoards.from_dict(s)


def team_board_list_to_dict(x: ListTeamBoards) -> dict:
    return x.to_dict()


def team_sprint_from_dict(s: Any) -> TeamSprint:
    return TeamSprint.from_dict(s)


def team_sprint_to_dict(x: TeamSprint) -> dict:
    return x.to_dict()


def team_sprint_list_from_dict(s: Any) -> ListTeamSprints:
    return ListTeamSprints.from_dict(s)


def team_sprint_list_to_dict(x: ListTeamSprints):
    return x.to_dict()
