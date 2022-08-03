from typing import Union
from .base import Serializer


class ContextSerializer(Serializer):
    """Context Serializer"""

    QUERY_PARAMS = {
        "limit": {"type": "integer", "coerce": int},
        "page": {"type": "integer", "coerce": int},
    }

    @classmethod
    def query_params(cls, params) -> Union[dict, list]:
        """Serialize query params.

        Args:
            params (dict): Query params.

        Returns:
            dict: Query params serialized.
        """
        if not params:
            return {}

        errors, data = cls._serialize(cls.QUERY_PARAMS, dict(params), purge=True)
        if errors:
            return {}
        return data
