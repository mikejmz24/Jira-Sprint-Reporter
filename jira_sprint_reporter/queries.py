import json
import os
from getpass import getpass

import requests
from dotenv import dotenv_values, load_dotenv

import entities.jira_issue
from entities.sprint_report_api import (
    SprintReport,
    sprint_report_from_dict,
    update_sprint_jira_issue_types,
)
from templates.sprint_report_template import sprint_report_template

config = dotenv_values("../.env")
load_dotenv()


def query_jira_issue(key: str) -> requests.Response:
    """Gets issue information from Jira and returns it as a
    requests.Response or requests.exceptions.ConnectionError"""
    base_url: str = "https://jira.amer.thermo.com/rest/api/2/issue/"
    headers: dict = {"Authorization": os.environ.get("PASSWORD")}

    return requests.request("GET", base_url + key, headers=headers)


def query_jira_issue_to_jira_issue_type(key: str) -> entities.jira_issue.JiraIssue:
    api_response: requests.Response = query_jira_issue(key)
    json_data = api_response.json()
    data_to_show = entities.jira_issue.jira_issue_from_dict(json_data)
    return data_to_show


def query_jira_issue_to_dict_or_json(key: str) -> dict:
    jira_issue_data: entities.jira_issue.JiraIssue = (
        query_jira_issue_to_jira_issue_type(key)
    )
    result: dict = entities.jira_issue.jira_issue_to_dict(jira_issue_data)
    return result


def create_confluence_page(ancestor: str, board: str) -> requests.Response:
    with open("../tests/json_files/sprint-36928.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        sprint_data: SprintReport = sprint_report_from_dict(data)
        sprint_data = update_sprint_jira_issue_types(sprint_data)
        base_url: str = "https://confluence.amer.thermo.com/rest/api/content"
        headers: dict = {
            "Accept": "application/json",
            "Authorization": os.environ.get("PASSWORD"),
            "Content-Type": "application/json",
        }
        content_value: str = sprint_report_template(sprint_data, board)
        print(content_value)
        data: dict = {
            "title": "Test from Python Requests",
            "type": "page",
            "space": {"key": "FIREGENE"},
            "status": "current",
            "ancestors": [{"id": ancestor}],
            "body": {
                "storage": {
                    "value": content_value,
                    "representation": "storage",
                }
            },
            "metadata": {"properties": {"editor": {"value": "v2"}}},
        }

        # return requests.request("POST", base_url, headers=headers, json=data)
        return requests.post(base_url, headers=headers, json=data)


def create_sprint_report_confluence_page() -> None:
    print("Enter your team's Jira Board ID")
    team_board: str = input()
    print("Type the ancestor ID where you want to create the confluence page")
    page: str = input()
    pswd: str = getpass("Enter your password:")
    res: requests.Response = create_confluence_page(page, team_board)
    print(f"status code: {res.status_code}")


def query_jira_issue_prompt() -> None:
    print("enter a jira issue to show the results on screen :) ")
    jira_issue = input()
    data: dict = query_jira_issue_to_dict_or_json(jira_issue)
    print(data)


if __name__ == "__main__":
    # TODO: Investigate how to login to Jira and how to navigate through teams boards and sprints.
    create_sprint_report_confluence_page()
