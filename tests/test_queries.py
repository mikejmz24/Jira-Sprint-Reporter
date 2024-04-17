import pytest
import requests

from jira_sprint_reporter import queries


def test_query_api() -> None:
    """Tests for a requests.exceptions.ConnectionError 519 when there is no VPN connection"""
    url: str = "INTGPT-109"
    with pytest.raises(requests.exceptions.ConnectionError) as excinfo:
        queries.query_jira_issue(url)
        assert excinfo.value.args[0] == 519
