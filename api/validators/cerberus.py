from typing import Tuple

from cerberus import Validator
from cerberus.schema import SchemaError

from api.configs import validator_configs
from api.validators.common import AdminSerializerSchema


ADMIN_SCHEMA = {
    "path": {"type": "string", "required": True},
    "schema": {"type": "dict", "required": True},
    "model": {"type": "string", "required": True},
}

admin_serializer = AdminSerializerSchema()


class Cerberus:
    """Cerberus Validator, contains validation methods."""

    @staticmethod
    def schema_is_valid(data) -> dict:
        """Validate if the schema is valid in cerberus.

        Args:
            data (dict): cerberus shema.

        Returns:
            dict: empty if was OK or errors if fail.
        """
        try:
            Validator(data)
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

        errors, body = admin_serializer.serialize(body)
        if errors:
            return errors, body
        return Cerberus.schema_is_valid(body.get("schema")), body
