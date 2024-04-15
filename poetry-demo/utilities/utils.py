from datetime import datetime
from typing import Any


def build_get_object_path(object_name: str, name: str) -> str:
    path_list: list[str] = name.split(".")
    result_string: str = object_name + '.get("'

    for element in path_list:
        result_string += element + '").get("'

    result_string = result_string[:-6]
    return result_string


def get_object_str(object_name: Any, path: str) -> str:
    path_list: list[str] = path.split(".")
    result: Any = object_name
    for element in path_list:
        result = result.get(element)
    return result


def get_object_list_of_str(object_name: Any, path: str) -> list[str]:
    path_list: list[str] = path.split(".")
    path_list_len: int = len(path_list)
    result: Any = object_name
    result_list: list[str] = []
    for index, element in enumerate(path_list):
        if index < path_list_len - 1:
            result = result.get(element)
    for item in result:
        result_list.append(item.get(path_list[path_list_len - 1]))
    return result_list


def get_object_datetime(
    object_name: Any, path: str, date_format: str = "%Y-%m-%dT%H:%M:%S"
) -> datetime:
    return datetime.strptime(get_object_str(object_name, path)[:-9], date_format)
