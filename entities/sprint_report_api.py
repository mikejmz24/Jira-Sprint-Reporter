"""
SprintReport
____________
An object that captures the most relevant data of the Jira sprint report rest api.
Notes
_____
https://jira.amer.thermo.com/rest/greenhopper/latest/rapid/charts/sprintreport?rapidViewId={}&sprintId={}
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from utilities import utils


@dataclass
class JiraIssueSprintReport:
    """ "
    The JiraIssueSpritnReport object captures the most relevant data of issues
    inside the Jira sprint report rest api

    ...
    Attributes
    __________
    key: str
        The issue key given by Jira.

    """

    jira_issue_id: int
    key: str
    issue_type: str
    summary: str
    assignee: str
    issue_status: str
    issue_priority: str
    resolution: str
    original_estimate: Optional[int] = None
    final_estimate: Optional[int] = None

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    @staticmethod
    def from_dict(obj: Any) -> "JiraIssueSprintReport":
        """
        Captures all the relevant fields from the Jira sprint report JSON response.

        Parameters
        __________
        key: str
            The given issue identification key string given by Jira.

        Returns
        _______
        JiraIssueSprintReport object
            A Python object with the selected Jira issue fields within the sprint report
            API response.
        """
        jira_issue_id: int = int(utils.get_object_str(obj, "id"))
        key: str = utils.get_object_str(obj, "key")
        issue_type: str = utils.get_object_str(obj, "typeId")
        summary: str = utils.get_object_str(obj, "summary")
        assignee: str = utils.get_object_str(obj, "assigneeName")
        issue_status: str = utils.get_object_str(obj, "statusId")
        issue_priority: str = utils.get_object_str(obj, "priorityId")
        resolution: str = utils.get_object(obj, "done")
        original_estimate: Optional[int] = utils.get_optional_int(
            obj, "currentEstimateStatistic.statFieldValue.value"
        )
        final_estimate: Optional[int] = utils.get_optional_int(
            obj, "estimateStatistic.statFieldValue.value"
        )
        return JiraIssueSprintReport(
            jira_issue_id,
            key,
            issue_type,
            summary,
            assignee,
            issue_status,
            issue_priority,
            resolution,
            original_estimate,
            final_estimate,
        )

    def to_dict(self) -> dict:
        """
        Returns the captured fields of the Jira issue within the sprint report rest api
        in a dict object.

        Returns
        _______
        A dict representtation of the JiraIssueSprintReport object.
        """
        result: dict = {}
        result["jira_issue_id"] = int(self.jira_issue_id)
        result["key"] = self.key
        result["issue_type"] = self.issue_type
        result["summary"] = self.summary
        result["assignee"] = self.assignee
        result["issue_status"] = self.issue_status
        result["issue_priority"] = self.issue_priority
        result["resolution"] = self.resolution
        if self.original_estimate is not None:
            result["original_estimate"] = int(self.original_estimate)
        if self.final_estimate is not None:
            result["final_estimate"] = int(self.final_estimate)
        return result

    def __repr__(self):
        return f"""
        jira_issue_id: {self.jira_issue_id}
        key: {self.key}
        issue_type: {self.issue_type}
        summary: {self.summary}
        assignee: {self.assignee}
        issue_status: {self.issue_status}
        issue_priority: {self.issue_priority}
        resolution: {self.resolution}
        original_estimate: {self.original_estimate}
        final_estimate: {self.final_estimate}"""


@dataclass
class SprintReport:
    """
    The SprintReport object captures the most relevant data of the Jira sprint report rest api.

    ...
    Atributes
    _________
    sprint_id: int
        The sprint id given by Jira.

    """

    sprint_id: int
    name: str
    goal: str
    start_date: datetime
    end_date: datetime
    status_types: dict
    priority_types: dict
    issue_types: dict
    commited_story_points: Optional[int]
    delivered_story_points: Optional[int]
    completed_issues: Optional[list[JiraIssueSprintReport]] = None
    not_completed_issues: Optional[list[JiraIssueSprintReport]] = None
    removed_issues: Optional[list[JiraIssueSprintReport]] = None
    issues_completed_outside: Optional[list[JiraIssueSprintReport]] = None
    added_issues: Optional[dict] = None

    @staticmethod
    def from_dict(obj: Any) -> "SprintReport":
        """
        Captures all the relevant fields from the original JSON resonse

        Parameters
        _________
        sprint_id: int
            The given identification number given by Jira.

        Returns
        _______
        SprintReport object
            A Python object with the selected fields.
        """
        sprint_id: int = int(utils.get_object_str(obj, "sprint.id"))
        name: str = utils.get_object_str(obj, "sprint.name")
        goal: str = utils.get_object_str(obj, "sprint.goal")
        start_date: datetime = utils.get_object_datetime_sprint_report(
            obj, "sprint.activatedDate"
        )
        end_date: datetime = utils.get_object_datetime_sprint_report(
            obj, "sprint.completeDate"
        )
        status_types: dict = utils.get_object(obj, "contents.entityData.statuses")
        priority_types: dict = utils.get_object(obj, "contents.entityData.priorities")
        issue_types: dict = utils.get_object(obj, "contents.entityData.types")
        commited_story_points: Optional[int] = utils.get_optional_int(
            obj, "contents.completedIssuesInitialEstimateSum.value"
        )
        delivered_story_points: Optional[int] = utils.get_optional_int(
            obj, "contents.completedIssuesEstimateSum.value"
        )
        completed_issues: Optional[list[JiraIssueSprintReport]] = (
            get_optional_jira_issue_sprint_report_list(obj, "contents.completedIssues")
        )
        not_completed_issues: Optional[list[JiraIssueSprintReport]] = (
            get_optional_jira_issue_sprint_report_list(
                obj, "contents.issuesNotCompletedInCurrentSprint"
            )
        )
        removed_issues: Optional[list[JiraIssueSprintReport]] = (
            get_optional_jira_issue_sprint_report_list(obj, "contents.puntedIssues")
        )
        issues_completed_outside: Optional[list[JiraIssueSprintReport]] = (
            get_optional_jira_issue_sprint_report_list(
                obj, "contents.issuesCompletedInAnotherSprint"
            )
        )
        added_issues: Optional[dict] = utils.get_object(
            obj, "contents.issueKeysAddedDuringSprint"
        )
        return SprintReport(
            sprint_id,
            name,
            goal,
            start_date,
            end_date,
            status_types,
            priority_types,
            issue_types,
            commited_story_points,
            delivered_story_points,
            completed_issues,
            not_completed_issues,
            removed_issues,
            issues_completed_outside,
            added_issues,
        )

    def to_dict(self) -> dict:
        """
        Returns the captured fields in a dict object.

        Returns
        _______
        A dict representation of a SprintReport object.
        """
        result: dict = {}
        result["sprint_id"] = str(self.sprint_id)
        result["name"] = self.name
        result["goal"] = self.goal
        result["start_date"] = str(self.start_date)
        result["end_date"] = str(self.end_date)
        # result["issue_types"] = self.issue_types
        result["commited_story_points"] = self.commited_story_points
        result["delivered_story_points"] = self.delivered_story_points
        result["completed_issues"] = self.completed_issues
        result["not_completed_issues"] = self.not_completed_issues
        result["removed_issues"] = self.removed_issues
        result["issues_completed_outside"] = self.issues_completed_outside
        result["added_issues"] = self.added_issues
        return result


def sprint_report_from_dict(s: Any) -> SprintReport:
    """
    Returns a SprintReport object

    Parameters
    __________
    s: Any
        JSON response from the Jira sprint report rest api.

    Returns
    _______
    SprintReport object
        The Python object contains the most relevant fields from the Jira
        rest api.
    """
    return SprintReport.from_dict(s)


def sprint_report_to_dict(x: SprintReport) -> dict:
    """
    Returns a dict object or that can be casted as a JSON.

    Parameters
    __________
    x: SprintReport
        SprintReport object

    Returns
    _______
    dict
        A dict with the data of the SprintReport object.
    """
    return x.to_dict()


def jira_issue_sprint_report_from_dict(s: Any) -> JiraIssueSprintReport:
    return JiraIssueSprintReport.from_dict(s)


def jira_issue_sprint_report_to_dict(s: JiraIssueSprintReport) -> dict:
    return JiraIssueSprintReport.to_dict(s)


def get_optional_jira_issue_sprint_report_list(
    object_name: Any, path: str
) -> Optional[list[JiraIssueSprintReport]]:
    result: Optional[list[JiraIssueSprintReport]] = None
    result = utils.get_optional_object(object_name, path)
    return (
        get_jira_issue_sprint_report_list(object_name, path)
        if result and len(result) > 0
        else None
    )


def get_jira_issue_sprint_report_list(
    object_name: Any, path: str
) -> list[JiraIssueSprintReport]:
    return [
        jira_issue_sprint_report_from_dict(item)
        for item in utils.get_object(object_name, path)
    ]


def get_all_jira_issues_from_sprint_report(
    object_name: SprintReport,
) -> list[JiraIssueSprintReport]:
    result: list[JiraIssueSprintReport] = []
    result = append_jira_issues_sprint_report(result, object_name.completed_issues)
    result = append_jira_issues_sprint_report(result, object_name.not_completed_issues)
    result = append_jira_issues_sprint_report(result, object_name.removed_issues)
    result = append_jira_issues_sprint_report(
        result, object_name.issues_completed_outside
    )
    return result


def append_jira_issues_sprint_report(
    result: list[JiraIssueSprintReport],
    items_list: Optional[list[JiraIssueSprintReport]],
) -> list[JiraIssueSprintReport]:
    if items_list:
        for item in items_list:
            result.append(item)
    return result


def get_jira_issues_with_estimation_change(
    sprint_data: SprintReport,
) -> Optional[list[JiraIssueSprintReport]]:
    result: Optional[list[JiraIssueSprintReport]] = []
    issues: Optional[list[JiraIssueSprintReport]] = (
        get_all_jira_issues_from_sprint_report(sprint_data)
    )
    if issues:
        for issue in issues:
            if (
                issue.final_estimate != issue.original_estimate
                or issue.final_estimate is None
            ):
                result.append(issue)
    return result


def clean_issue_types(obj: dict, name: str) -> dict:
    res: dict = {}
    if obj is not None:
        res = {item: data.get(name) for item, data in obj.items()}
    return res


def set_issue_type(
    jira_issue: JiraIssueSprintReport, types: dict, name: str
) -> JiraIssueSprintReport:
    access_name: str = name.split("_")[1]
    print(f"access_name with initial split: {access_name}")
    access_name = f"{access_name}Name"
    print(f"access_name after concatenation: {access_name}")
    types = clean_issue_types(types, access_name)
    print(types)
    for type_key, type_value in types.items():
        if jira_issue[name] == type_key:
            jira_issue[name] = type_value
    return jira_issue


def update_sprint_jira_issue_types(sprint: SprintReport) -> SprintReport:
    sprint.status_types = clean_issue_types(sprint.status_types, "statusName")
    sprint.priority_types = clean_issue_types(sprint.priority_types, "priorityName")
    sprint.issue_types = clean_issue_types(sprint.issue_types, "typeName")
    sprint.completed_issues = update_sprint_issue_keys_with_values(
        sprint.completed_issues, sprint
    )
    sprint.not_completed_issues = update_sprint_issue_keys_with_values(
        sprint.not_completed_issues, sprint
    )
    sprint.removed_issues = update_sprint_issue_keys_with_values(
        sprint.removed_issues, sprint
    )
    sprint.issues_completed_outside = update_sprint_issue_keys_with_values(
        sprint.issues_completed_outside, sprint
    )
    return sprint


def update_issue_key_with_value(
    issue: JiraIssueSprintReport, original: dict, name: str
) -> str:
    for clean_key, clean_value in original.items():
        if issue[name] == clean_key:
            issue[name] = clean_value
    return issue[name]


def update_sprint_issue_keys_with_values(
    issue_list: Optional[list[JiraIssueSprintReport]], original: SprintReport
) -> Optional[list[JiraIssueSprintReport]]:
    if issue_list is not None:
        for issue in issue_list:
            issue.issue_status = update_issue_key_with_value(
                issue, original.status_types, "issue_status"
            )
            issue.issue_priority = update_issue_key_with_value(
                issue, original.priority_types, "issue_priority"
            )
            issue.issue_type = update_issue_key_with_value(
                issue, original.issue_types, "issue_type"
            )
    return issue_list


def get_active_developers(sprint: SprintReport) -> set:
    issue_list: list[JiraIssueSprintReport] = get_all_jira_issues_from_sprint_report(
        sprint
    )
    return {item.assignee for item in issue_list if item.assignee != "None"}


def get_added_issues(
    added_dict: Optional[dict], issues: list[JiraIssueSprintReport]
) -> Optional[list[JiraIssueSprintReport]]:
    # res: list[JiraIssueSprintReport] = []
    # if added_dict is not None:
    #     res = [issue for issue in issues if issue["key"] in added_dict]
    # return res
    #
    if added_dict is None:
        return None
    return list(filter(lambda issue: issue["key"] in added_dict, issues))


def get_total_commited_pbis(sprint: SprintReport) -> int:
    if sprint.completed_issues is None:
        return 0

    if sprint.added_issues is not None:
        added_keys: set = set(sprint.added_issues.keys())
        commited_issues: list[JiraIssueSprintReport] = [
            issue for issue in sprint.completed_issues if issue["key"] not in added_keys
        ]
        return len(commited_issues)

    return len(sprint.completed_issues)


def get_original_commited_issues(sprint: SprintReport) -> list[JiraIssueSprintReport]:
    if sprint.completed_issues is None and sprint.removed_issues is None:
        return []

    added_keys: set = set()

    if sprint.added_issues is not None:
        added_keys = set(sprint.added_issues.keys())

    commited_issues: list[JiraIssueSprintReport] = []

    if sprint.completed_issues is not None:
        commited_issues += [
            issue for issue in sprint.completed_issues if issue["key"] not in added_keys
        ]

    if sprint.removed_issues is not None:
        commited_issues += list(sprint.removed_issues)

    return commited_issues
