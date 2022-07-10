from cerberus import Validator


class ContextSerializer:
    """Context Serializer"""

    QUERY_PARAMS = {
        "limit": {"type": "integer", "coerce": int},
        "page": {"type": "integer", "coerce": int},
    }

    @classmethod
    def query_params_normalize(cls, params):
        """Normalize query params

        Args:
            params (dict): query params not serialized.

        Returns:
            dict: Data serialized.
        """
        if not params:
            return {}
        v = Validator(cls.QUERY_PARAMS, purge_unknown=True)
        return v.normalized(dict(params))
