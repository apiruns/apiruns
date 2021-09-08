import uuid
from typing import List, Tuple, Any


def paths_with_slash(path) -> List[str]:
    """Build path with slashes"""
    path_two = path[:-1] if path.endswith("/") else f"{path}/"
    return [path, path_two]


def build_path_from_params(params: tuple) -> Tuple[str, str, Any]:
    """Receives request parameters and splits it into different paths.

    Args:
        params (tuple): Tuple of request params.

    Returns:
        (str, str, str): Return origin path, path modified and uuid.
    """
    if validate_uuid(params[-1]):
        _id = params[-1]
        original = f"/{'/'.join(params)}"
        modified = f"/{'/'.join(params[:-1])}"
        return original, modified, _id

    original = f"/{'/'.join(params)}"
    return original, original, None


def validate_uuid(value: str) -> bool:
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
