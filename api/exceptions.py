from typing import Union


class BaseException(Exception):
    """Base Exception"""

    def __init__(self, content: Union[dict, list], status_code: int):
        """
        Args:
            content (Union[dict, list]): response objects.
            status_code (int): custom status code.
        """
        self.content = content
        self.status_code = status_code
