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
    summary: str
    original_estimate: int
    final_estimate: Optional[int] = None

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
        summary: str = utils.get_object_str(obj, "key")
        # original_estimate: int = int(
        #     utils.get_object_str(obj, "currentEstimateStatistic.statFieldValue.value")
        # )
        original_estimate: int = utils.get_object_int(
            obj, "currentEstimateStatistic.statFieldValue.value"
        )
        final_estimate: Optional[int] = utils.get_optional_int(
            obj, "estimateStatistic.statFieldValue.value"
        )
        return JiraIssueSprintReport(
            jira_issue_id, key, summary, original_estimate, final_estimate
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
        result["key"] = str(self.key)
        result["summary"] = str(self.summary)
        result["original_estimate"] = int(self.original_estimate)
        if self.final_estimate is not None:
            result["final_estimate"] = int(self.final_estimate)
        return result


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

    ## TODO: Add the rest of the SprintReport fields
    ## Add method to clean the types with only the key and name
    sprint_id: int
    name: str
    goal: str
    start_date: datetime
    end_date: datetime
    issue_types: dict
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
        issue_types: dict = utils.get_object(obj, "contents.entityData.types")
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
            issue_types,
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
        result["issue_types"] = self.issue_types
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
    return get_jira_issue_sprint_report_list(object_name, path) if result else None


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
            if issue.final_estimate != issue.original_estimate:
                result.append(issue)
    return result
