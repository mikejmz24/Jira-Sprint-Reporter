import json

from utilities import utils


def test_get_object_path_str() -> None:
    object_name: str = "object"
    original_path: str = "fields.components.name"
    full_result_path: str = 'object.get("fields").get("components").get("name")'
    assert utils.build_get_object_path(object_name, original_path) == full_result_path


def test_get_object_string_with_no_levels_of_nested_search() -> None:
    with open("json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        search_path: str = "key"
        expected_result: str = "INTGPT-109"
        assert utils.get_object_str(data, search_path) == expected_result


def test_get_object_string_with_three_levels_of_nested_search() -> None:
    with open("json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        search_path: str = "fields.priority.name"
        expected_result: str = "P2 - High"
        assert utils.get_object_str(data, search_path) == expected_result


def test_get_object_list_of_string_with_one_item() -> None:
    with open("json_files/intgpt-109.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        search_path: str = "fields.components.name"
        expected_result: list[str] = ["Global Launch"]
        assert utils.get_object_list_of_str(data, search_path) == expected_result


def test_base64_encodes_login_credentials() -> None:
    res: str = (
        "bWlndWVsLmppbWVuZXoyQHRoZXJtb2Zpc2hlci5jb206IVRoM3JtQEYxc2gzclNjMTNudDFmMWMyMDIyLi4="
    )
    assert (
        utils.encode_login_credentials(
            "miguel.jimenez2@thermofisher.com", "!Th3rm@F1sh3rSc13nt1f1c2022.."
        )
        == res
    )
