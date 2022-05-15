from api.serializers import Serializer


class AuthXSerializer(Serializer):
    """AuthX Serializer"""

    # validations
    CERBERUS_USER_SCHEMA = {
        "email": {
            "required": False,
            "type": "string",
            "regex": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        },
        "username": {
            "required": True,
            "type": "string",
            "regex": r"^[a-zA-Z0-9_]*$",
        },
        "password": {
            "type": "string",
            "required": True,
            "regex": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$",  # no-qa
        },
    }
    CERBERUS_SIGN_IN_SCHEMA = {
        "username": {
            "type": "string",
            "regex": r"^[a-zA-Z0-9_]*$",
            "required": True,
        },
        "password": {
            "required": True,
            "type": "string",
        },
    }

    @classmethod
    def validate_register(cls, body: dict):
        """Validate register.

        Args:
            body (dict): request body.

        Returns:
            dict: errors.
        """
        return cls.is_valid(cls.CERBERUS_SIGN_IN_SCHEMA, body)

    @classmethod
    def validate_login(cls, body: dict):
        """Validate login.

        Args:
            body (dict): request body.

        Returns:
            dict: errors.
        """
        return cls.is_valid(cls.CERBERUS_USER_SCHEMA, body)
