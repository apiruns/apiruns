import uuid
from typing import Tuple
from typing import Union

from .base import Serializer
from api.configs import app_configs
from api.datastructures import Model


class CoreSerializer(Serializer):
    """Core Serializer"""

    @classmethod
    def model(
        cls, body: dict, schema: dict, is_update: bool = False
    ) -> Tuple[Union[dict, None], Union[None, Model]]:
        """Serialize model.

        Args:
            body (dict): request body.
            schema (dict): cerberus schema.

        Returns:
            Tuple[Union[dict, None], Union[None, Model]]:
                Returns errors and data serialized.
        """
        errors = cls._validate_schema(schema)
        if errors:
            return errors, None

        errors, data = cls._serialize(schema, body, purge=True)
        if errors:
            return errors, None

        if not is_update:
            data[app_configs.IDENTIFIER_ID] = str(uuid.uuid4())
            return None, data

        return None, data
