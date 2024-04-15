from dataclasses import dataclass
from datetime import datetime
from typing import Any

from utilities import utils


@dataclass
class JiraIssue:
    issue_id: int
    key: str
    summary: str
    issue_type: str
    priority: str
    components: list[str]
    labels: list[str]
    # sprint: list[str]
    status: str
    resolution: str
    fix_version: list[str]
    description: str
    assignee: str
    reporter: str
    created: datetime
    updated: datetime
    resolved: datetime

    @staticmethod
    def from_dict(obj: Any):
        issue_id: int = int(utils.get_object_str(obj, "id"))
        key: str = utils.get_object_str(obj, "key")
        summary: str = utils.get_object_str(obj, "fields.summary")
        issue_type: str = utils.get_object_str(obj, "fields.issuetype.name")
        priority: str = utils.get_object_str(obj, "fields.priority.name")
        components: list[str] = utils.get_object_list_of_str(
            obj, "fields.components.name"
        )
        labels: list[str] = utils.get_object_list_of_str(obj, "fields.labels.name")
        status: str = utils.get_object_str(obj, "fields.status.name")
        resolution: str = utils.get_object_str(obj, "fields.resolution.name")
        description: str = utils.get_object_str(obj, "fields.description")
        fix_versions: list[str] = utils.get_object_list_of_str(
            obj, "fields.fixVersions.name"
        )
        assignee: str = utils.get_object_str(obj, "fields.assignee.name")
        reporter: str = utils.get_object_str(obj, "fields.reporter.name")
        created: datetime = utils.get_object_datetime(obj, "fields.created")
        updated: datetime = utils.get_object_datetime(obj, "fields.updated")
        resolved: datetime = utils.get_object_datetime(obj, "fields.resolutiondate")
        return JiraIssue(
            issue_id,
            key,
            summary,
            issue_type,
            priority,
            components,
            labels,
            status,
            resolution,
            fix_versions,
            description,
            assignee,
            reporter,
            created,
            updated,
            resolved,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["issue_id"] = str(self.issue_id)
        result["key"] = self.key
        result["summary"] = self.summary
        result["issue_type"] = self.issue_type
        result["priority"] = self.priority
        result["components"] = self.components
        result["labels"] = self.labels
        result["status"] = self.status
        result["resolution"] = self.resolution
        result["fix_versions"] = self.fix_version
        result["description"] = self.description
        result["assignee"] = self.assignee
        result["reporter"] = self.reporter
        result["created"] = str(self.created)
        result["updated"] = str(self.updated)
        result["resolved"] = str(self.resolved)
        return result


def jira_issue_from_dict(s: Any) -> JiraIssue:
    return JiraIssue.from_dict(s)


def jira_issue_to_dict(x: JiraIssue) -> dict:
    return x.to_dict()
