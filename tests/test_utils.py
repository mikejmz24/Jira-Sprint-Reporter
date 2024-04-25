import json
from typing import Generator, Optional

import pytest

from entities import sprint_report_api
from utilities import utils


class TestUtilsMethodsWithInternalJSONFile:
    @pytest.fixture(scope="class")
    def sprint_data(self) -> Generator[sprint_report_api.SprintReport, None, None]:
        with open("json_files/sprint-36928.json", encoding="utf-8") as json_file:
            data = json.load(json_file)
            yield sprint_report_api.sprint_report_from_dict(data)

    def test_get_all_jira_items_list(
        self, sprint_data: sprint_report_api.SprintReport
    ) -> None:
        jira_issues: Optional[list[sprint_report_api.JiraIssueSprintReport]] = (
            sprint_report_api.get_all_jira_issues_from_sprint_report(sprint_data)
        )
        result: int = len(jira_issues) if jira_issues else 0
        assert result == 10


def test_get_object_path_str() -> None:
    object_name: str = "object"
    original_path: str = "fields.components.name"
    full_result_path: str = 'object.get("fields").get("components").get("name")'
    assert utils.build_get_object_path(object_name, original_path) == full_result_path


def test_get_object_string_with_no_levels_of_nested_search() -> None:
    with open("json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        search_path: str = "key"
        expected_result: str = "INTGPT-109"
        assert utils.get_object_str(data, search_path) == expected_result


def test_get_object_string_with_three_levels_of_nested_search() -> None:
    with open("json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        search_path: str = "fields.priority.name"
        expected_result: str = "P2 - High"
        assert utils.get_object_str(data, search_path) == expected_result


def test_get_object_list_of_string_with_one_item() -> None:
    with open("json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        search_path: str = "fields.components.name"
        expected_result: list[str] = ["Global Launch"]
        assert utils.get_object_list_of_str(data, search_path) == expected_result
