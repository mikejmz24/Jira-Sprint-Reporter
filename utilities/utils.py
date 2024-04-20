from datetime import datetime
from typing import Any, Optional

from entities import sprint_report_api


def get_object(object_name: Any, path: str) -> object:
    path_list: list[str] = path.split(".")
    result: Any = object_name
    for element in path_list:
        result = result.get(element)
    return result


def build_get_object_path(object_name: str, name: str) -> str:
    path_list: list[str] = name.split(".")
    result_string: str = object_name + '.get("'

    for element in path_list:
        result_string += element + '").get("'

    result_string = result_string[:-6]
    return result_string


def get_object_str(object_name: Any, path: str) -> str:
    path_list: list[str] = path.split(".")
    result: Any = object_name
    for element in path_list:
        result = result.get(element)
    return result


def get_object_list_of_str(object_name: Any, path: str) -> list[str]:
    path_list: list[str] = path.split(".")
    path_list_len: int = len(path_list)
    result: Any = object_name
    result_list: list[str] = []
    for index, element in enumerate(path_list):
        if index < path_list_len - 1:
            result = result.get(element)
    for item in result:
        result_list.append(item.get(path_list[path_list_len - 1]))
    return result_list


def get_object_simple_list(object_name: Any, path: str) -> list[str]:
    result_list: list[str] = []
    result: Any = get_object(object_name, path)
    for item in result:
        result_list.append(item)
    return result_list


def get_jira_issue_sprint_report_list(
    object_name: Any, path: str
) -> list[sprint_report_api.JiraIssueSprintReport]:
    result_list: list[sprint_report_api.JiraIssueSprintReport] = []
    result: Any = get_object(object_name, path)
    for item in result:
        completed_issue: sprint_report_api.JiraIssueSprintReport = (
            sprint_report_api.JiraIssueSprintReport.from_dict(item)
        )
        result_list.append(completed_issue)
    return result_list


def get_object_datetime(
    object_name: Any, path: str, date_format: str = "%Y-%m-%dT%H:%M:%S"
) -> datetime:
    return datetime.strptime(get_object_str(object_name, path)[:-9], date_format)


def get_object_datetime_sprint_report(
    object_name: Any, path: str, date_format: str = "%d/%b/%y %H:%M %p"
) -> datetime:
    datetime_str: str = get_object_str(object_name, path)
    print(datetime_str)
    if len(datetime_str) < 18:
        datetime_str = datetime_str[:10] + "1" + datetime_str[10:]
    return datetime.strptime(get_object_str(object_name, path), date_format)


def get_optional_object(object_name: Any, path: str) -> Optional[object]:
    result: Optional[object] = get_object(object_name, path)
    return result


def get_optional_str(object_name: Any, path: str) -> Optional[str]:
    result: Optional[str] = str(get_object(object_name, path))
    return result


def get_optional_int(object_name: Any, path: str) -> Optional[int]:
    result: Optional[int] = (
        int(get_object_str(object_name, path))
        if get_object(object_name, path)
        else None
    )
    return result


def get_optional_datetime(object_name: Any, path: str) -> Optional[datetime]:
    result: Optional[datetime] = get_object_datetime(object_name, path)
    return result


def get_optional_jira_issue_sprint_report_list(
    object_name: Any, path: str
) -> Optional[list[sprint_report_api.JiraIssueSprintReport]]:
    result: Optional[list[sprint_report_api.JiraIssueSprintReport]] = None
    if get_object(object_name, path):
        result: Optional[list[sprint_report_api.JiraIssueSprintReport]] = (
            get_jira_issue_sprint_report_list(object_name, path)
        )
    return result
