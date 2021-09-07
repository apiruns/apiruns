from typing import List


def paths_with_slash(path) -> List[str]:
    """Build path with slashes"""
    path_two = path[:-1] if path.endswith("/") else f"{path}/"
    return [path, path_two]
