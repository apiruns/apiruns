from cerberus import Validator
from cerberus.schema import SchemaError
from api.constants import ValidationErrorResponse
from api.validators.base import ValidatorMixin


class CerberusValidator(ValidatorMixin):
    """Validator of schema with cerberus"""

    @staticmethod
    def schema(data):
        """Validate schema."""
        try:
            Validator(data)
            return
        except SchemaError as e:
            return e

    @staticmethod
    def payload(schema, data):
        """Validate payload wih schema."""
        if not len(data):
            return ValidationErrorResponse.PAYLOAD_NULL

        v = Validator(schema)
        v.validate(data)
        return v.errors
