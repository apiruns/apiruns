from unittest.mock import patch

from cerberus.schema import SchemaError

from api.validators.cerberus import Cerberus


def test_cerberus_validator_schema_error_null():
    schema = {"name": {"type": "string", "maxleng": 10}}
    response = Cerberus.schema_is_valid(schema)
    expected = {"name": [{"maxleng": ["unknown rule"]}]}
    assert len(response) != 0
    assert isinstance(response, dict)
    assert response == expected


def test_cerberus_validator_schema_valid():
    schema = {"name": {"type": "string", "maxlength": 10}}
    response = Cerberus.schema_is_valid(schema)
    assert isinstance(response, dict)
    assert len(response) == 0


def test_cerberus_validator_payload_error_data_type():
    schema = {"name": {"type": "string", "maxlength": 10}}
    data = {"name": 0}
    response = Cerberus.data_is_valid(schema, data)
    expected = {"name": ["must be of string type"]}
    assert len(response) != 0
    assert isinstance(response, dict)
    assert response == expected


def test_cerberus_validator_payload_success():
    schema = {"name": {"type": "string", "maxlength": 10}}
    data = {"name": "pepe"}
    response = Cerberus.data_is_valid(schema, data)
    assert isinstance(response, dict)
    assert len(response) == 0


def test_cerberus_invalid_schema_admin_by_required():
    payload = {"path": "/", "model": "root", "schema": {}}
    expected = [{"schema": "schema is type object and not empty."}]
    error, body = Cerberus.admin_model(payload)
    assert len(error) != 0
    assert error == expected


@patch("api.validators.cerberus.AdminSerializerSchema.serialize")
def test_cerberus_invalid_schema_admin_by_serializer_error(serializer_mock):
    payload = {
        "path": "/user12",
        "model": "root",
        "schema": {"username": {"type": "string"}},
    }
    serializer_mock.return_value = (
        [{"error": "the path must only contain letters and the '/' character."}],
        payload,
    )

    errors, body = Cerberus.admin_model(payload)
    assert len(errors) != 0
    serializer_mock.assert_called_once_with(payload)


@patch("api.validators.cerberus.AdminSerializerSchema.serialize")
def test_cerberus_schema_admin_valid(serializer_mock):
    payload = {
        "path": "/users",
        "model": "root",
        "schema": {"username": {"type": "string"}},
    }
    serializer_mock.return_value = ([], payload)

    errors, body = Cerberus.admin_model(payload)
    assert len(errors) == 0
    assert body == payload
    serializer_mock.assert_called_once_with(payload)
