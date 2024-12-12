import base64
import os
from datetime import datetime
from typing import Any, Optional

# def get_absolute_path(relative_path: str, base_path: Optional[str] = None) -> str:
#     """Returns the absolute path for a given relative path."""
#     if base_path is None:
#         # base_path = os.path.dirname(os.path.abspath(__file__))
#         base_path = os.path.dirname(os.path.dirname(__file__))
#     return os.path.join(base_path, relative_path)


# def get_project_root() -> str:
#     """Returns the root directory of the project."""
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     while not os.path.isfile(os.path.join(current_dir, "main.py")):
#         current_dir = os.path.dirname(current_dir)
#         if current_dir == os.path.dirname(current_dir):  # Reached the filesystem root
#             raise FileNotFoundError("Project root with 'main.py' not found.")
#     return current_dir
#
#
# def get_relative_path(relative_path: str, base_path: Optional[str] = None) -> str:
#     """Returns the relative path at the root of the project for a given relative path."""
#     if base_path is None:
#         base_path = get_project_root()
#     absolute_path = os.path.join(base_path, relative_path)
#     project_root = get_project_root()
#     return os.path.relpath(absolute_path, start=project_root)
def get_project_root() -> str:
    """
    Returns the absolute path to the project root directory.
    The root is identified by the presence of a 'main.py' file.

    Returns:
        str: Absolute path to the project root directory

    Raises:
        FileNotFoundError: If the project root containing 'main.py' cannot be found
    """
    # Get the absolute path of the directory containing this utility file
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)

    # Search upwards until we find main.py or hit the filesystem root
    while True:
        if os.path.isfile(os.path.join(current_dir, "main.py")):
            return current_dir

        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Reached filesystem root
            raise FileNotFoundError(
                f"Project root with 'main.py' not found when searching upwards from {current_file}"
            )
        current_dir = parent_dir


def get_absolute_path(relative_path: str, base_path: Optional[str] = None) -> str:
    """
    Converts a relative path to an absolute path based on the project root.

    Args:
        relative_path (str): The relative path to convert
        base_path (Optional[str]): Base path to use instead of project root

    Returns:
        str: The absolute path
    """
    if base_path is None:
        base_path = get_project_root()
    return os.path.abspath(os.path.join(base_path, relative_path))


def get_relative_path(path: str, base_path: Optional[str] = None) -> str:
    """
    Converts any path to a path relative to the project root.

    Args:
        path (str): The path to convert (can be absolute or relative)
        base_path (Optional[str]): Base path to use instead of project root

    Returns:
        str: The relative path from the project root
    """
    if base_path is None:
        base_path = get_project_root()

    # First convert the input path to absolute
    abs_path = get_absolute_path(path, os.path.dirname(os.path.abspath(path)))

    # Then get the relative path from the base
    return os.path.relpath(abs_path, start=base_path)


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
    object_name: Any,
    path: str,
    date_format: str = "%Y-%m-%dT%H:%M:%S",
    str_len: int = -9,
) -> datetime:
    return datetime.strptime(get_object_str(object_name, path)[:str_len], date_format)


def get_object_datetime_sprint_report(
    object_name: Any, path: str, date_format: str = "%d/%b/%y %H:%M %p"
) -> datetime:
    datetime_str: str = get_object(object_name, path)
    if len(datetime_str) < 18:
        datetime_str = datetime_str[:10] + "1" + datetime_str[10:]
    return datetime.strptime(datetime_str, date_format)


def get_optional_object(object_name: Any, path: str) -> Optional[Any]:
    object_exists: Any = get_object(object_name, path)
    return object_exists if object_exists else None


def get_optional_str(object_name: Any, path: str) -> Optional[str]:
    object_exists: Any = get_object(object_name, path)
    return str(object_exists) if object_exists else None


def get_optional_int(object_name: Any, path: str) -> Optional[int]:
    result = get_object(object_name, path)
    return int(result) if result else None


def get_optional_datetime(
    object_name: Any, path: str, str_len: int = -9
) -> Optional[datetime]:
    object_exists: Any = get_object(object_name, path)
    return (
        get_object_datetime(object_name, path, str_len=str_len)
        if object_exists
        else None
    )


def encode_login_credentials(user_name: str, password: str) -> str:
    res: str = f"{user_name}:{password}"
    res_bytes = res.encode("ascii")
    res_encoded: bytes = base64.b64encode(res_bytes)
    return res_encoded.decode("utf-8")
