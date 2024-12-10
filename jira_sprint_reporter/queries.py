import json
import os
import sys
from getpass import getpass
from typing import Tuple

import requests
from dotenv import dotenv_values, load_dotenv

import entities.jira_issue
from entities.sprint_report_api import (
    SprintReport,
    sprint_report_from_dict,
    update_sprint_jira_issue_types,
)
from entities.team_info import (
    ListTeamBoards,
    ListTeamSprints,
    TeamBoard,
    TeamSprint,
    team_board_list_from_dict,
    team_sprint_list_from_dict,
)
from templates.sprint_report_template import sprint_report_template
from utilities.utils import encode_login_credentials

config = dotenv_values("../.env")
load_dotenv()

# headers: dict = {"Authorikzation": os.environ.get("PASSWORD")}
headers_data: dict = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": os.environ.get("BEARER_TOKEN"),
    "Cookie": os.environ.get("COOKIE"),
}


def query_jira_issue(key: str) -> requests.Response:
    """Gets issue information from Jira and returns it as a
    requests.Response or requests.exceptions.ConnectionError"""
    base_url: str = "https://jira.amer.thermo.com/rest/api/2/issue/"
    headers = headers_data
    # headers: dict = {"Authorikzation": os.environ.get("PASSWORD")}

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
    result: dict = jira_issue_data.to_dict()
    return result


def create_confluence_page(ancestor: str, board: str) -> requests.Response:
    with open("../tests/json_files/sprint-36928.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        sprint_data: SprintReport = sprint_report_from_dict(data)
        sprint_data = update_sprint_jira_issue_types(sprint_data)
        base_url: str = "https://confluence.amer.thermo.com/rest/api/content"
        # headers: dict = {
        #     "Accept": "application/json",
        #     "Authorization": os.environ.get("PASSWORD"),
        #     "Content-Type": "application/json",
        # }
        headers = headers_data
        content_value: str = sprint_report_template(sprint_data, board)
        data: dict = {
            "title": f"{sprint_data.name} Sprint Report – Generated via Python Script",
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


def create_confluence_page_with_params(
    creds: str, board: str, sprint: str, space: str, ancestor: str
) -> requests.Response:
    base_url: str = (
        f"https://jira.amer.thermo.com/rest/greenhopper/latest/rapid/charts/sprintreport?rapidViewId={board}&sprintId={sprint}"
    )
    sprint_data_response: requests.Response = make_api_request(creds, base_url, "GET")
    # sprint_data_response: requests.Response = make_api_request_bearer(base_url, "GET")
    sprint_data: SprintReport = sprint_report_from_dict(sprint_data_response.json())
    sprint_data = update_sprint_jira_issue_types(sprint_data)
    base_url: str = "https://confluence.amer.thermo.com/rest/api/content"
    headers: dict = {
        "Accept": "application/json",
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
    }
    # headers = headers_data
    content_value: str = sprint_report_template(sprint_data, board)
    data: dict = {
        "title": f"{sprint_data.name} Sprint Report – Generated via Python Script",
        "type": "page",
        "space": {"key": space},
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
    # headers: dict = {
    #     "Accept": "application/json",
    #     "Authorization": f"Basic {authorization}",
    #     "Content-Type": "application/json",
    # }
    headers = headers_data
    return requests.request(request_type, base_url, headers=headers)


def make_api_request_bearer(
    base_url: str, request_type: str = "POST"
) -> requests.Response:
    headers = {
        k: v.encode("utf-8") if isinstance(v, str) else v
        for k, v in headers_data.items()
    }
    return requests.request(request_type, base_url, headers=headers)


def select_board_and_sprint(psswrd: str) -> Tuple[str, str]:
    team_board_id = select_team_board(psswrd)
    sprint_id = select_team_sprint(psswrd, team_board_id)
    return team_board_id, sprint_id


def select_team_board(psswrd: str) -> str:
    print("Search for a team board that you would like to generate reports")
    team_board: str = input()
    board_api: str = (
        f"https://jira.amer.thermo.com/rest/agile/latest/board?&startAt=0&name={team_board}"
    )
    # board_response: requests.Response = make_api_request(psswrd, board_api, "GET")
    board_response: requests.Response = make_api_request_bearer(board_api, "GET")
    if board_response.status_code == 200:
        list_team_board_object: ListTeamBoards = team_board_list_from_dict(
            board_response.json()
        )
        team_selection: dict[str, str] = select_item(
            list_team_board_object.boards, "team board"
        )
        print(
            f"Excellent, we can continue! Your team board number is: {team_selection['id']}"
        )
        return team_selection["id"]
    print(f"There was an error with the board. HTTP code: {board_response.status_code}")
    sys.exit()


def select_team_sprint(psswrd: str, team_board_id: str) -> str:
    sprint_api: str = (
        # f"https://jira.amer.thermo.com/rest/agile/latest/board/{team_board_id}/sprint?maxResults=9&startAt=0"
        f"https://jira.amer.thermo.com/rest/agile/latest/board/{team_board_id}/sprint?startAt=0"
    )
    # sprint_response: requests.Response = make_api_request(psswrd, sprint_api, "GET")
    sprint_response: requests.Response = make_api_request_bearer(sprint_api, "GET")
    if sprint_response.status_code == 200:
        list_team_sprints_object: ListTeamSprints = team_sprint_list_from_dict(
            sprint_response.json()
        )
        sprint_selection: dict[str, str] = select_item(
            list_team_sprints_object.sprints, "sprint"
        )
        print(
            f"Excellent, we can continue! Your sprint number is: {sprint_selection['id']}"
        )
        return sprint_selection["id"]
    print(
        f"There was an error with the sprints. HTTP code: {sprint_response.status_code}"
    )
    sys.exit()


def create_sprint_report_with_user_interaction() -> None:
    psswrd: str = f"{os.environ.get("PASSWORD")}"
    team_board_id, sprint_id = select_board_and_sprint(psswrd)

    print(
        "Now finally enter the Confluence Space and Ancestor IDs where you would like to create the Sprint report"
    )
    print("First enter the Confluence Space Key")
    space: str = input()
    print("Now let's finish with the Confluence Ancestor ID")
    ancestor: str = input()
    confluence_page_response: requests.Response = create_confluence_page_with_params(
        psswrd,
        team_board_id,
        sprint_id,
        space,
        ancestor,
    )
    print(f"Confluence page HTTP response code: {confluence_page_response.status_code}")


def select_item(
    items: list[TeamBoard] | list[TeamSprint],
    item_type: str,
) -> dict[str, str]:
    print(f"Please select a {item_type}:")
    for index, item in enumerate(items):
        print(f"[{index + 1}] {item.name}")
    user_selection_index: int = int(input(f"Enter the number of the {item_type}: "))
    selected_item: TeamBoard | TeamSprint = items[user_selection_index - 1]
    return {
        "id": (
            str(selected_item.team_board_id)
            if isinstance(selected_item, TeamBoard)
            else str(selected_item.sprint_id)
        ),
        "name": selected_item.name,
    }


def ask_user_to_login() -> list[str]:
    print("Enter your Thermo Fisher username (complete email address)")
    user_name: str = input()
    password: str = getpass("Enter you Thermo Fisher password")
    test_url: str = (
        "https://jira.amer.thermo.com/rest/agile/latest/board?maxResults=1&startAt=0&name=qppi"
    )
    encrypted_credentials: str = encode_login_credentials(user_name, password)
    # test_response = make_api_request(encrypted_credentials, test_url, "GET")
    test_response = make_api_request_bearer(test_url, "GET")
    return [encrypted_credentials, str(test_response.status_code)]


if __name__ == "__main__":
    create_sprint_report_with_user_interaction()
    # create_sprint_report_confluence_page()
