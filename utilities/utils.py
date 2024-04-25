from datetime import datetime
from typing import Any, Optional


def get_object(object_name: Any, path: str) -> Any:
    for element in path.split("."):
        object_name = object_name.get(element)
    return object_name


def build_get_object_path(object_name: str, name: str) -> str:
    path_list: list[str] = name.split(".")
    result_string: str = object_name + '.get("'

    for element in path_list:
        result_string += element + '").get("'

    result_string = result_string[:-6]
    return result_string


def get_object_str(object_name: Any, path: str) -> str:
    return str(get_object(object_name, path))


def get_object_int(object_name: Any, path: str) -> int:
    return int(float(get_object_str(object_name, path)))


def get_object_list_of_str(object_name: Any, path: str) -> list[str]:
    path_list: list[str] = path.split(".")
    path_list_len: int = len(path_list)
    for index, element in enumerate(path.split(".")):
        if index < path_list_len - 1:
            object_name = object_name.get(element)
    return [item.get(path_list[path_list_len - 1]) for item in object_name]


def get_object_simple_list(object_name: Any, path: str) -> list[str]:
    return list(get_object(object_name, path))


def get_object_datetime(
    object_name: Any, path: str, date_format: str = "%Y-%m-%dT%H:%M:%S"
) -> datetime:
    return datetime.strptime(get_object_str(object_name, path)[:-9], date_format)


def get_object_datetime_sprint_report(
    object_name: Any, path: str, date_format: str = "%d/%b/%y %H:%M %p"
) -> datetime:
    datetime_str: str = get_object(object_name, path)
    if len(datetime_str) < 18:
        datetime_str = datetime_str[:10] + "1" + datetime_str[10:]
    return datetime.strptime(datetime_str, date_format)


def get_optional_object(object_name: Any, path: str) -> Optional[Any]:
    return get_object(object_name, path)


def get_optional_str(object_name: Any, path: str) -> Optional[str]:
    return str(get_object(object_name, path))


def get_optional_int(object_name: Any, path: str) -> Optional[int]:
    result = get_object(object_name, path)
    return int(result) if result else None


def get_optional_datetime(object_name: Any, path: str) -> Optional[datetime]:
    return get_object_datetime(object_name, path)
