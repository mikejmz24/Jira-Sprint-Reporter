import json

from entities import jira_issue


def test_jira_issue_from_dict_returns_jira_issue_object_type() -> None:
    """jira_issue_from_dict method returns a valid JiraIssue object type
    when a valid JSON is passed as a parameter"""
    with open("json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        json_data: jira_issue.JiraIssue = jira_issue.jira_issue_from_dict(data)
        print("str() string: ", str(json_data))

        print("repr() string: ", repr(json_data))
        assert isinstance(json_data, jira_issue.JiraIssue)
