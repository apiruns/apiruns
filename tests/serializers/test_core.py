from unittest.mock import patch

from api.serializers.core import CoreSerializer


class TestCoreSerializer:
    def test_core_schema_invalid(self):
        # Mocks
        schema = {"user": "str"}
        body = {"user": "anybody"}
        # process
        errors, data = CoreSerializer.model(body, schema)
        # asserts
        assert errors == {"user": ["must be of dict type"]}
        assert data == None

    def test_core_error_validating_data(self):
        # Mocks
        schema = {"user": {"type": "string", "required": True}}
        # process
        errors, data = CoreSerializer.model({}, schema)
        # asserts
        assert errors == {"user": ["required field"]}
        assert data == None

    def test_core_success_with_update(self):
        # Mocks
        schema = {"user": {"type": "string", "required": True}}
        body = {"user": "anybody", "public_id": "u123"}
        # process
        errors, data = CoreSerializer.model(body, schema, is_update=True)
        # asserts
        assert errors == None
        assert data == {"user": "anybody"}

    @patch("api.serializers.core.uuid.uuid4")
    def test_core_success_with_not_update(self, mock_uuid):
        # Mocks
        mock_uuid.return_value = "M123"
        schema = {"user": {"type": "string", "required": True}}
        body = {"user": "anybody", "public_id": "u123"}
        # process
        errors, data = CoreSerializer.model(body, schema, is_update=False)
        # asserts
        assert errors == None
        assert data == {"public_id": "M123", "user": "anybody"}
        mock_uuid.assert_called_once_with()
