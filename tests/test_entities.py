import json
import os
from typing import Generator, Optional

import pytest

from entities.jira_issue import JiraIssue, jira_issue_from_dict, jira_issue_to_dict
from entities.sprint_report_api import (
    JiraIssueSprintReport,
    SprintReport,
    clean_issue_types,
    get_active_developers,
    get_all_jira_issues_from_sprint_report,
    get_jira_issues_with_estimation_change,
    set_issue_type,
    sprint_report_from_dict,
    update_issue_key_with_value,
)
from entities.team_info import (
    ListTeamBoards,
    ListTeamSprints,
    team_board_list_from_dict,
    team_sprint_list_from_dict,
)
from jira_sprint_reporter.sprint_report_queries import get_sprint_report_data
from utilities.utils import get_absolute_path


def test_jira_issue_from_dict_returns_jira_issue_object_type() -> None:
    """jira_issue_from_dict method returns a valid JiraIssue object type
    when a valid JSON is passed as a parameter"""
    json_file_path: str = get_absolute_path("tests/json_files/intgpt-109.json")
    with open(json_file_path, encoding="utf-8") as json_file:
        data = json.load(json_file)
        json_data: JiraIssue = jira_issue_from_dict(data)
        print("str() string: ", str(json_data))

        print("repr() string: ", repr(json_data))
        assert isinstance(json_data, JiraIssue)


def test_jira_issue_to_dict_returns_json_object_type() -> None:
    """jira_issue_to_dict method return a valid Json object type
    when a valid JiraIssue object is passed as parameter"""
    json_file_path: str = get_absolute_path("tests/json_files/intgpt-109.json")
    with open(json_file_path, encoding="utf-8") as json_file:
        data = json.load(json_file)
        print(type(data))
        json_data: JiraIssue = jira_issue_from_dict(data)
        json_response = jira_issue_to_dict(json_data)
        print(json_response)
        assert isinstance(json_response, dict)


def test_sprint_report_from_dict_returns_sprint_report_object_type() -> None:
    """sprint_report_api_to_dict method returns a valid SprintReport object type
    when a valid JSON object is passed as parameter"""
    json_file_path: str = get_absolute_path("tests/json_files/intgpt-109.json")
    with open(json_file_path, encoding="utf-8") as json_file:
        data = json.load(json_file)
        json_data: SprintReport = sprint_report_from_dict(data)
        print("str() string: ", str(json_data))

        print("repr() string: ", repr(json_data))
        assert isinstance(json_data, SprintReport)


class TestSprintReportMethods:
    @pytest.fixture(scope="class")
    def sprint_data(self) -> Generator[SprintReport, None, None]:
        json_file_path: str = get_absolute_path("tests/json_files/sprint-36928.json")
        with open(json_file_path, encoding="utf-8") as json_file:
            data = json.load(json_file)
            yield sprint_report_from_dict(data)

    def test_return_statuses_dict(self, sprint_data: SprintReport) -> None:
        statuses: dict = clean_issue_types(sprint_data.status_types, "statusName")
        print(statuses)
        assert len(statuses) == 3

    def test_return_priorities_dict(self, sprint_data: SprintReport) -> None:
        priorities: dict = clean_issue_types(sprint_data.priority_types, "priorityName")
        print(priorities)
        assert len(priorities) == 2

    def test_return_types_dict(self, sprint_data: SprintReport) -> None:
        issues: dict = clean_issue_types(sprint_data.issue_types, "typeName")
        print(issues)
        assert len(issues) == 5

    def test_get_all_jira_items_list(self, sprint_data: SprintReport) -> None:
        jira_issues: Optional[list[JiraIssueSprintReport]] = (
            get_all_jira_issues_from_sprint_report(sprint_data)
        )
        result: int = len(jira_issues) if jira_issues else 0
        assert result == 10

    def test_set_jira_status_type(self, sprint_data: SprintReport) -> None:
        if sprint_data.completed_issues is not None:
            completed_issue: Optional[JiraIssueSprintReport] = (
                sprint_data.completed_issues[2]
            )
            result: JiraIssueSprintReport = set_issue_type(
                completed_issue, sprint_data.issue_types, "issue_type"
            )
            assert result.issue_type == "Bug"

    def test_set_jira_issue_priority(self, sprint_data: SprintReport) -> None:
        if sprint_data.completed_issues is not None:
            completed_issue: Optional[JiraIssueSprintReport] = (
                sprint_data.completed_issues[2]
            )
            result: JiraIssueSprintReport = set_issue_type(
                completed_issue, sprint_data.priority_types, "issue_priority"
            )
            assert result.issue_priority == "P2 - High"

    def test_set_jira_issue_status(self, sprint_data: SprintReport) -> None:
        if sprint_data.completed_issues is not None:
            completed_issue: Optional[JiraIssueSprintReport] = (
                sprint_data.completed_issues[2]
            )
            result: JiraIssueSprintReport = set_issue_type(
                completed_issue, sprint_data.status_types, "issue_status"
            )
            assert result.issue_status == "Resolved"

    def test_get_all_sprint_developers(self, sprint_data) -> None:
        result: set = get_active_developers(sprint_data)
        assert len(result) == 4

    def test_update_issue_value(self, sprint_data) -> None:
        sprint_data.issue_types = clean_issue_types(sprint_data.issue_types, "typeName")
        issue: JiraIssueSprintReport = sprint_data.completed_issues[0]
        result: str = update_issue_key_with_value(
            issue, sprint_data.issue_types, "issue_type"
        )
        assert result == "Story"


# TODO: Review failing tests with calls to real API
class TestQuerySprintReport:
    @pytest.fixture(scope="class")
    def sprint_data(self) -> Generator[SprintReport, None, None]:
        yield get_sprint_report_data("6363", "36928")

    def test_sprint_36928_returns_eight_completed_issues(
        self, sprint_data: SprintReport
    ) -> None:
        result: int = (
            len(sprint_data.completed_issues) if sprint_data.completed_issues else 0
        )
        assert result == 8

    def test_sprint_36928_returns_one_not_completed_issues(
        self, sprint_data: SprintReport
    ) -> None:
        result: int = (
            len(sprint_data.not_completed_issues)
            if sprint_data.not_completed_issues
            else 0
        )
        assert result == 1

    def test_sprint_36928_returns_one_issue_removed_from_sprint(
        self, sprint_data: SprintReport
    ) -> None:
        result: int = (
            len(sprint_data.removed_issues) if sprint_data.removed_issues else 0
        )
        assert result == 1

    def test_sprint_36928_returns_four_issues_added_to_sprint(
        self, sprint_data: SprintReport
    ) -> None:
        result: int = len(sprint_data.added_issues) if sprint_data.added_issues else 0
        assert result == 4

    def test_sprint_36928_returns_three_issues_with_changed_estimations(
        self, sprint_data
    ) -> None:
        issue_list: Optional[list[JiraIssueSprintReport]] = (
            get_jira_issues_with_estimation_change(sprint_data)
        )
        result: int = len(issue_list) if issue_list else 0
        assert result == 4


class TestTeamBoard:
    @pytest.fixture(scope="class")
    def boards(self) -> Generator[ListTeamBoards, None, None]:
        json_file_path: str = get_absolute_path("tests/json_files/qppi-boards.json")
        with open(json_file_path, encoding="utf-8") as json_file:
            data = json.load(json_file)
            yield team_board_list_from_dict(data)

    def test_team_board_list_returns_team_board_list_object(self, boards) -> None:
        assert isinstance(boards, ListTeamBoards)


class TestTeamSprint:
    @pytest.fixture(scope="class")
    def sprint(self) -> Generator[ListTeamSprints, None, None]:
        json_file_path: str = get_absolute_path("tests/json_files/6363-sprints.json")
        with open(json_file_path, encoding="utf-8") as json_file:
            data = json.load(json_file)
            yield team_sprint_list_from_dict(data)

    def test_team_sprint_returns_team_sprint_object(self, sprint) -> None:
        assert isinstance(sprint, ListTeamSprints)
