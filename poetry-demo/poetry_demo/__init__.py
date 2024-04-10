import os

import requests
from dotenv import dotenv_values, load_dotenv

config = dotenv_values("../.env")
load_dotenv()


def query_jira_issue(
    key: str,
) -> requests.Response | requests.exceptions.ConnectionError:
    """Gets issue information from Jira and returns it as a
    requests.Response or requests.exceptions.ConnectionError"""
    base_url: str = "https://jira.amer.thermo.com/rest/api/2/issue/"
    headers: dict = {"Authorization": os.environ.get("PASSWORD")}

    return requests.request("GET", base_url + key, headers=headers)
