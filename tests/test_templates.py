import json
from typing import Generator

import pytest

from entities.sprint_report_api import SprintReport, sprint_report_from_dict


class TestSprintReportMethods:
    @pytest.fixture(scope="class")
    def sprint_data(self) -> Generator[SprintReport, None, None]:
        with open("json_files/sprint-36928.json", encoding="utf-8") as json_file:
            data = json.load(json_file)
            yield sprint_report_from_dict(data)

    def test_sprint_report_template_includes_sprint_name(self, sprint_data) -> None:
        res: str = sprint_data.name
        name: str = "Gene.AI Delivery Sprint 12"
        assert name in res
