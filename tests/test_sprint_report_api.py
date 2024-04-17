import json

from entities import sprint_report_api


def test_sprint_report_from_dict_returns_sprint_report_object_type() -> None:
    """sprint_report_api_from_dict method returns a valid SprintReport object type
    when a valid JSON is pased as a parameter"""
    with open("json_files/sprint-36928.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        json_data: sprint_report_api.SprintReport = (
            sprint_report_api.sprint_report_from_dict(data)
        )
        assert isinstance(json_data, sprint_report_api.SprintReport)
