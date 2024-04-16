import os

import requests
from dotenv import dotenv_values, load_dotenv

import entities.jira_issue

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


if __name__ == "__main__":
    print("enter a jira issue to show the results on screen :) ")
    jira_issue = input()
    data: entities.jira_issue.JiraIssue = query_jira_issue_to_jira_issue_type(
        jira_issue
    )
    print(data)
