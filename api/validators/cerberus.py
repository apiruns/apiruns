from typing import Tuple

from cerberus import Validator
from cerberus.schema import SchemaError
from dacite import from_dict

from api.configs import validator_configs
from api.datastructures import Model


ADMIN_SCHEMA = {
    "path": {
        "type": "string",
        "required": True,
        "empty": False,
        "minlength": 1,
        "regex": "^/|/[a-z0-9]+(?:/[a-z0-9]+|/)*$",
    },
    "model": {
        "type": "string",
        "maxlength": 70,
        "regex": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
    },
    "schema": {
        "type": "dict",
        "required": True,
        "empty": False,
        "minlength": 1
    },
}


class Cerberus:
    """Cerberus Validator, contains validation methods."""

    @staticmethod
    def schema_is_valid(schema) -> dict:
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

    @staticmethod
    def data_is_valid(schema, body) -> dict:
        """Validate the datos vs the schema.

        Args:
            schema (dict): cerberus schema.
            body (dict): data.

        Returns:
            dict: empty if was OK or errors if fail.
        """
        if not len(body):
            return validator_configs.ValidationErrorResponse.PAYLOAD_NULL

        v = Validator(schema)
        v.validate(body)
        return v.errors

    @staticmethod
    def admin_model(body) -> Tuple[dict, dict]:
        """Validate the model admin.

        Args:
            body (dict): Data to validate.

        Returns:
            Tuple[dict, dict]: errors and body serialized.
        """
        error = Cerberus.data_is_valid(ADMIN_SCHEMA, body)
        if error:
            return error, body

        model = from_dict(data_class=Model, data=body)

        return Cerberus.schema_is_valid(model.schema), model.to_json()
