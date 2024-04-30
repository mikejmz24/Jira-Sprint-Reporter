import json
import os

import requests
from dotenv import dotenv_values, load_dotenv

import entities.jira_issue
from entities.sprint_report_api import SprintReport, sprint_report_from_dict
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


def create_confluence_page(ancestor: str) -> requests.Response:
    with open("../tests/json_files/sprint-36928.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        sprint_data = sprint_report_from_dict(data)
        base_url: str = "https://confluence.amer.thermo.com/rest/api/content"
        headers: dict = {
            "Accept": "application/json",
            "Authorization": os.environ.get("PASSWORD"),
            "Content-Type": "application/json",
        }
        # content_value: str = """
        # <h1>This is a content added from a Python script</h1>
        # This is a normal paragraph test...
        # <br /><br />
        #
        # This below is a macro<br />
        # <ac:structured-macro ac:name="info">
        # <ac:parameter ac:name="title">Info Macro Title</ac:parameter>
        # <ac:rich-text-body>
        # Some text goes inside the macro...
        # </ac:rich-text-body>
        # </ac:structured-macro>
        # """
        content_value: str = sprint_report_template(sprint_data)
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


if __name__ == "__main__":
    # print("enter a jira issue to show the results on screen :) ")
    # jira_issue = input()
    # data: dict = query_jira_issue_to_dict_or_json(jira_issue)
    # print(data)
    print("Type the ancestor where to create the confluence page")
    page = input()
    res: requests.Response = create_confluence_page(page)
    print(f"status code: {res.status_code}")
