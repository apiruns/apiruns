import uuid
from datetime import date
from datetime import datetime
from typing import Tuple
from typing import Union


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def get_or_create_model(name) -> str:
    """Get or create model name with uuid.

    Args:
        name (str): Model name.

    Returns:
        str: Original name or uuid name.
    """
    if not name:
        u = uuid.uuid4()
        return f"model_{str(u)}"
    return name


def paths_without_slash(path: str) -> str:
    """Build path without slashes"""
    return path[:-1] if path.endswith("/") else path


def split_uuid_path(path) -> Tuple[str, Union[str, None]]:
    """Split in origin path for get uuid.

    Args:
        path (str): Origin path.

    Returns:
        Tuple[str, Union[str, None]]: path and uuid.
    """
    split = path.split("/")
    if is_uuid_valid(split[-1]):
        path = "/".join(split[:-1])
        return path, split[-1]
    return paths_without_slash(path), None


def is_uuid_valid(value: str) -> bool:
    """Validate if is uuid.

    Args:
        value (str): uuid.

    Returns:
        bool: true if is valid else false.
    """
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False
