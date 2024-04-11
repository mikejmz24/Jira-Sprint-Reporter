from dataclasses import dataclass
from datetime import datetime
from typing import Any


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
        date_format: str = "%Y-%m-%dT%H:%M:%S"
        issue_id: int = int(obj.get("id"))
        key: str = obj.get("key")
        summary: str = obj.get("fields").get("summary")
        issue_type: str = obj.get("fields").get("issuetype").get("name")
        priority: str = obj.get("fields").get("priority").get("name")
        component_items: list[dict] = obj.get("fields").get("components")
        components = []
        if component_items is not None:
            for component in component_items:
                components.append(component.get("name"))
        label_items: list[dict] = obj.get("fields").get("labels")
        labels = []
        if label_items is not None:
            for label in label_items:
                labels.append(label.get("name"))
        # sprints: list[str] = []
        # for sprint in obj.get()
        status: str = obj.get("fields").get("status").get("name")
        resolution: str = obj.get("fields").get("resolution").get("name")
        fix_version_items: list[dict] = obj.get("fields").get("fixVersions")
        fix_versions = []
        if fix_version_items is not None:
            for fix_version in fix_version_items:
                fix_versions.append(fix_version.get("name"))
        description: str = obj.get("fields").get("description")
        assignee: str = obj.get("fields").get("assignee").get("name")
        reporter: str = obj.get("fields").get("reporter").get("name")
        created: datetime = datetime.strptime(
            obj.get("fields").get("created")[:-9], date_format
        )
        updated: datetime = datetime.strptime(
            obj.get("fields").get("updated")[:-9], date_format
        )
        resolved: datetime = datetime.strptime(
            obj.get("fields").get("resolutiondate")[:-9], date_format
        )
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
        result["created"] = self.created
        result["updated"] = self.updated
        result["resolved"] = self.resolved
        return result


def jira_issue_from_dict(s: Any) -> JiraIssue:
    return JiraIssue.from_dict(s)


def jira_issue_to_dict(x: JiraIssue) -> dict:
    return x.to_dict()
