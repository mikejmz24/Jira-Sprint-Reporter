import os
from typing import Optional

import requests
from dotenv import dotenv_values, load_dotenv

from entities.sprint_report_api import (
    JiraIssueSprintReport,
    SprintReport,
    sprint_report_from_dict,
)

config = dotenv_values("../.env")
load_dotenv()


class QuerySprintReport:
    def query_sprint_data(self, sprint_board: str, sprint_id: str) -> requests.Response:
        base_url: str = (
            "https://jira.amer.thermo.com/rest/greenhopper/latest/rapid/charts/sprintreport?rapidViewId="
        )
        # headers: dict = {"Authorization": os.environ.get("PASSWORD")}
        headers: dict = {"Authorization": os.environ.get("PASSWORD")}

        return requests.request(
            "GET", base_url + sprint_board + "&sprintId=" + sprint_id, headers=headers
        )


def get_sprint_report_data(sprint_board: str, sprint_id: str) -> SprintReport:
    query_sprint_report: QuerySprintReport = QuerySprintReport()
    request_data: requests.Response = QuerySprintReport.query_sprint_data(
        query_sprint_report, sprint_board, sprint_id
    )
    json_data = request_data.json()
    sprint_report_data: SprintReport = sprint_report_from_dict(json_data)
    return sprint_report_data


def get_completed_issues(
    sprint_board: str, sprint_id: str
) -> Optional[list[JiraIssueSprintReport]]:
    sprint_report_data: SprintReport = get_sprint_report_data(sprint_board, sprint_id)
    completed_issues: Optional[list[JiraIssueSprintReport]] = (
        sprint_report_data.completed_issues
    )
    return completed_issues


def get_not_completed_issues(
    sprint_board: str, sprint_id: str
) -> Optional[list[JiraIssueSprintReport]]:
    sprint_report_data: SprintReport = get_sprint_report_data(sprint_board, sprint_id)
    not_completed_issues: Optional[list[JiraIssueSprintReport]] = (
        sprint_report_data.not_completed_issues
    )
    return not_completed_issues
