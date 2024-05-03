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
from entities.team_info import ListTeamBoards, TeamBoard, team_board_list_from_dict
from templates.sprint_report_template import sprint_report_template
from utilities.utils import encode_login_credentials

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
    res: requests.Response = create_confluence_page(page, team_board)
    print(f"status code: {res.status_code}")


def query_jira_issue_prompt() -> None:
    print("enter a jira issue to show the results on screen :) ")
    jira_issue = input()
    data: dict = query_jira_issue_to_dict_or_json(jira_issue)
    print(data)


def make_api_request(
    authorization: str, base_url: str, request_type: str = "POST"
) -> requests.Response:
    headers: dict = {
        "Accept": "application/json",
        "Authorization": f"Basic {authorization}",
        "Content-Type": "application/json",
    }
    return requests.request(request_type, base_url, headers=headers)


def create_sprint_report_with_user_interaction() -> None:
    # creds: list[str] = ask_user_to_login()
    # while creds[1] != "200":
    #     print("There was a problem logging you in. Please try again...")
    #     creds = ask_user_to_login()
    # print("Excellent you're now logged in!")
    print("Search for a team board that you would like to generate reports")
    team_board: str = input()
    board_api: str = (
        f"https://jira.amer.thermo.com/rest/agile/latest/board?&startAt=0&name={team_board}"
    )
    # board_response: requests.Response = make_api_request(creds[0], board_api, "GET")
    board_response: requests.Response = make_api_request(
        "bWlndWVsLmppbWVuZXoyQHRoZXJtb2Zpc2hlci5jb206IVRoM3JtQEYxc2gzclNjMTNudDFmMWMyMDIyLi4=",
        board_api,
        "GET",
    )
    list_team_board_object: ListTeamBoards = team_board_list_from_dict(
        board_response.json()
    )
    team_selection: TeamBoard = user_board_select(list_team_board_object)
    print("Excellent, we can continue!")
    print(team_selection)
    # for index, team in enumerate(list_team_board_object.boards):
    #     if user_team_select == str(index + 1):
    #         print(f"Thanks for your selection: {team.name}")


def user_board_select(list_team_board_object: ListTeamBoards) -> TeamBoard:
    while True:
        print("Please select a team:")
        for index, team in enumerate(list_team_board_object.boards):
            print(f"[{index + 1}] {team.name}")
        user_team_select: str = input("Enter the number of the team: ")
        if user_team_select in map(
            str, range(1, len(list_team_board_object.boards) + 1)
        ):
            selected_team: TeamBoard = list_team_board_object.boards[
                int(user_team_select) - 1
            ]
            print(f"Thanks for your selection: {selected_team.name}")
            return selected_team
        print("Sorry, invalid input. Please select a valid team number.")


def ask_user_to_login() -> list[str]:
    print("Enter your Thermo Fisher username (complete email address)")
    user_name: str = input()
    password: str = getpass("Enter you Thermo Fisher password")
    test_url: str = (
        "https://jira.amer.thermo.com/rest/agile/latest/board?maxResults=1&startAt=0&name=qppi"
    )
    encrypted_credentials: str = encode_login_credentials(user_name, password)
    test_response = make_api_request(encrypted_credentials, test_url, "GET")
    return [encrypted_credentials, str(test_response.status_code)]


if __name__ == "__main__":
    create_sprint_report_with_user_interaction()
    # create_sprint_report_confluence_page()
