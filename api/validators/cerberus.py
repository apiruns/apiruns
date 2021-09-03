from cerberus import Validator
from cerberus.schema import SchemaError
from api.constants import ValidationErrorResponse


class CerberusValidator:

    @staticmethod
    def schema(data):
        try:
            Validator(data)
            return
        except SchemaError as e:
            return e

    @staticmethod
    def payload(schema, data):
        if not len(data):
            return ValidationErrorResponse.PAYLOAD_NULL

        v = Validator(schema)
        v.validate(data)
        return v.errors
