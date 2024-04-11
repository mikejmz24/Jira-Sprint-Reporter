import json

from entities import jira_issue


def test_jira_issue_returns_json_data_when_json_is_provided() -> None:
    with open("../tests/json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        json_data = jira_issue.jira_issue_from_dict(data)
        print(json_data)
        assert json_data is not None
