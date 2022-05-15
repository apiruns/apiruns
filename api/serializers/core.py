import uuid
from typing import Any
from typing import Tuple

from api.configs import app_configs
from api.serializers import Serializer


class CoreSerializer(Serializer):
    """Core Serializer"""

    @classmethod
    def validate(cls, body: dict, schema: dict) -> Tuple[bool, Any]:
        """Validate core.

        Args:
            body (dict): request body.
            schema (dict): schema.

        Returns:
            Tuple[bool, Any]: is valid and errors.
        """
        valid, errors = cls.validate_core(body, schema)
        if not valid:
            return False, errors

        body[app_configs.IDENTIFIER_ID] = str(uuid.uuid4())
        return True, body

    @classmethod
    def validate_update(cls, body: dict, schema: dict) -> Tuple[bool, Any]:
        """Validate update core.

        Args:
            body (dict): request body.
            schema (dict): schema.

        Returns:
            Tuple[bool, Any]: is valid and errors.
        """
        valid, errors = cls.validate_core(body, schema)
        if not valid:
            return False, errors

        if app_configs.IDENTIFIER_ID in body:
            del body[app_configs.IDENTIFIER_ID]

        return True, body
