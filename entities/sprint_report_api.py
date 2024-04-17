from dataclasses import dataclass
from typing import Any

from utilities import utils


@dataclass
class SprintReport:
    sprint_id: int

    @staticmethod
    def from_dict(obj: Any):
        sprint_id: int = int(utils.get_object_str(obj, "sprint.id"))
        return SprintReport(sprint_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sprint_id"] = str(self.sprint_id)
        return result


def sprint_report_from_dict(s: Any) -> SprintReport:
    return SprintReport.from_dict(s)


def sprint_report_to_dict(x: SprintReport) -> dict:
    return x.to_dict()
