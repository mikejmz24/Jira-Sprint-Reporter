import json
from typing import Optional

import requests

from entities import jira_issue, sprint_report_api
from jira_sprint_reporter import sprint_report_queries


def test_jira_issue_from_dict_returns_jira_issue_object_type() -> None:
    """jira_issue_from_dict method returns a valid JiraIssue object type
    when a valid JSON is passed as a parameter"""
    with open("json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        json_data: jira_issue.JiraIssue = jira_issue.jira_issue_from_dict(data)
        print("str() string: ", str(json_data))

        print("repr() string: ", repr(json_data))
        assert isinstance(json_data, jira_issue.JiraIssue)


def test_jira_issue_to_dict_returns_json_object_type() -> None:
    """jira_issue_to_dict method return a valid Json object type
    when a valid JiraIssue object is passed as parameter"""
    with open("json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        print(type(data))
        json_data: jira_issue.JiraIssue = jira_issue.jira_issue_from_dict(data)
        json_response = jira_issue.jira_issue_to_dict(json_data)
        print(json_response)
        assert isinstance(json_response, dict)


def test_sprint_report_from_dict_returns_sprint_report_object_type() -> None:
    """sprint_report_api_to_dict method returns a valid SprintReport object type
    when a valid JSON object is passed as parameter"""
    with open("json_files/sprint-36928.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        json_data: sprint_report_api.SprintReport = (
            sprint_report_api.sprint_report_from_dict(data)
        )
        print("str() string: ", str(json_data))

        print("repr() string: ", repr(json_data))
        assert isinstance(json_data, sprint_report_api.SprintReport)


class TestQuerySprintReport:
    def test_sprint_36928_returns_eight_completed_issues(self) -> None:
        sprint_36928_data: sprint_report_api.SprintReport = (
            sprint_report_queries.get_sprint_report_data("6363", "36928")
        )
        sprint_36928_completed_issues: Optional[
            list[sprint_report_api.JiraIssueSprintReport]
        ] = sprint_36928_data.completed_issues
        result: int = (
            len(sprint_36928_completed_issues) if sprint_36928_completed_issues else 0
        )
        assert result == 8

    def test_sprint_36928_returns_one_not_completed_issues(self) -> None:
        sprint_36928_data: sprint_report_api.SprintReport = (
            sprint_report_queries.get_sprint_report_data("6363", "36928")
        )
        sprint_36928_completed_issues: Optional[
            list[sprint_report_api.JiraIssueSprintReport]
        ] = sprint_36928_data.not_completed_issues
        result: int = (
            len(sprint_36928_completed_issues) if sprint_36928_completed_issues else 0
        )
        assert result == 1

    # def test_sprint_36928_returns_one_issue_removed_from_sprint(self) -> None:
    #     assert False
    #
    # def test_sprint_36928_returns_four_issues_added_to_sprint(self) -> None:
    #     assert False
    #
    # def test_sprint_36928_returns_three_issues_with_changed_estimations(self) -> None:
    #     assert False
