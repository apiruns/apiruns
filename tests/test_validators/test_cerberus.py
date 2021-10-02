from cerberus.schema import SchemaError

from api.validators.cerberus import CerberusValidator


def test_cerberus_validator_schema_error_null():
    schema = {"name": {"type": "string", "maxleng": 10}}
    response = CerberusValidator.schema(schema)
    assert response != None
    assert isinstance(response, SchemaError)


def test_cerberus_validator_schema_valid():
    schema = {"name": {"type": "string", "maxlength": 10}}
    response = CerberusValidator.schema(schema)
    assert response == None


def test_cerberus_validator_payload_error_data_type():
    schema = {"name": {"type": "string", "maxlength": 10}}
    data = {"name": 0}
    response = CerberusValidator.payload(schema, data)
    expected = {"name": ["must be of string type"]}
    assert isinstance(response, dict)
    assert response == expected
