from typing import Tuple
from typing import Union

from dacite import from_dict

from .base import Cerberus
from .utils import status_code_allowed
from .utils import upper
from api.configs import route_config
from api.datastructures import Model


class AdminSerializer(Cerberus):
    """Admin Serializer"""

    MODEL_SCHEMA = {
        "path": {
            "type": "string",
            "required": True,
            "empty": False,
            "minlength": 1,
            "regex": "^/|/[a-z0-9]+(?:/[a-z0-9]+|/)*$",
        },
        "name": {
            "type": "string",
            "maxlength": 70,
            "regex": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
        },
        "schema": {"type": "dict", "required": True, "empty": False, "minlength": 1},
        "status_code": {
            "type": "dict",
            "required": False,
            "empty": False,
            "keysrules": {
                "type": "string",
                "allowed": route_config.HTTPMethod.to_list(),
                "coerce": (str, upper()),
            },
            "valuesrules": {"type": "integer", "allowed": status_code_allowed()},
        },
        "static": {
            "type": "dict",
            "required": False,
            "empty": False,
            "keysrules": {
                "type": "string",
                "allowed": route_config.HTTPMethod.static(),
                "coerce": (str, upper()),
            },  # TODO: validate json valid.
        },
    }
    DELETE_MODEL = {
        "name": {
            "type": "string",
            "required": True,
        },
    }

    @classmethod
    def model(cls, body: dict) -> Tuple[Union[dict, None], Union[None, Model]]:
        """Serialize model.

        Args:
            body (dict): request body.

        Returns:
            Tuple[Union[dict, None], Union[None, Model]]: Returns errors and model object.
        """
        errors = cls._validate_schema(body.get("schema"))
        if errors:
            return errors, None

        errors, data = cls._serialize(cls.MODEL_SCHEMA, body, purge=True)
        if errors:
            return errors, None

        model = from_dict(data_class=Model, data=data)
        return None, model

    @classmethod
    def delete_model(cls, body: dict) -> Tuple[dict, Union[dict, list]]:
        """Serialize delete model.

        Args:
            body (dict): request body.

        Returns:
            Tuple[dict, Union[dict, list]]: Returns errors and data serialized.
        """
        return cls._serialize(cls.DELETE_MODEL, body, purge=True)
