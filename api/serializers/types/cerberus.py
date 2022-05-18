from typing import Any
from typing import Tuple

from cerberus import Validator
from cerberus.schema import SchemaError

from .validations import status_code_allowed
from .validations import upper
from api.configs import route_config


ADMIN_SCHEMA = {
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

ADMIN_DELETE_PATH = {
    "path": {
        "type": "string",
        "minlength": 1,
        "regex": "^/|/[a-z0-9]+(?:/[a-z0-9]+|/)*$",
    }
}
ADMIN_DELETE_MODEL = {
    "model": {
        "type": "string",
        "maxlength": 70,
        "regex": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
    },
}


class Cerberus:
    """Cerberus Validator, contains validation methods."""

    @classmethod
    def schema_is_valid(cls, schema) -> dict:
        """Validate if the schema is valid in cerberus.

        Args:
            data (dict): cerberus schema.

        Returns:
            dict: empty if was OK or errors if fail.
        """
        try:
            Validator(schema)
            return {}
        except SchemaError as e:
            return e.args[0]

    @classmethod
    def is_valid(cls, schema, body) -> dict:
        """Validate the datos vs the schema.

        Args:
            schema (dict): cerberus schema.
            body (dict): data.

        Returns:
            dict: empty if was OK or errors if fail.
        """
        v = Validator(schema, purge_unknown=True)
        v.validate(body)
        return v.errors

    @classmethod
    def validate_model(cls, body) -> Tuple[bool, Any]:
        errors = cls.schema_is_valid(body.get("schema"))
        if errors:
            return False, errors

        errors = cls.is_valid(ADMIN_SCHEMA, body)
        if errors:
            return False, errors

        return True, None

    @classmethod
    def validate_core(cls, body, schema) -> Tuple[bool, Any]:
        errors = cls.schema_is_valid(schema)
        if errors:
            return False, errors

        errors = cls.is_valid(schema, body)
        if errors:
            return False, errors

        return True, None

    @classmethod
    def validate_delete_model(cls, body) -> Tuple[bool, Any]:
        errors = cls.is_valid(ADMIN_DELETE_MODEL, body)
        if errors:
            return False, errors

        return True, None
