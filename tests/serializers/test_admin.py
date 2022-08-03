from api.datastructures import Model
from api.serializers.admin import AdminSerializer


class TestAdminSerializer:
    def test_model_schema_invalid(self):
        # Mocks
        body = {"schema": {"name": "string"}, "path": "/users"}
        # process
        error, model = AdminSerializer.model(body)
        # asserts
        assert error == {"name": ["must be of dict type"]}
        assert model == None

    def test_mock_schema_valid_with_wrong_struture(self):
        # Mocks
        body = {
            "schema": {"user": {"type": "string"}},
        }
        # process
        error, model = AdminSerializer.model(body)
        # asserts
        assert error == {"path": ["required field"]}
        assert model == None

    def test_mock_with_success_full_data(self):
        # Mocks
        body = {
            "path": "/users",
            "name": "user",
            "schema": {"name": {"type": "string", "required": True}},
            "status_code": {"get": 200},
            "static": {"get": {"mock": "i'm a mock"}},
        }
        # process
        error, model = AdminSerializer.model(body)
        # asserts
        assert error == None
        assert isinstance(model, Model)
        assert model.path == "/users"

    def test_delete_model_with_error(self):
        # Mocks
        body = {"names": "121212"}
        # process
        error, data = AdminSerializer.delete_model(body)
        # asserts
        assert error == {"name": ["required field"]}
        assert data == {}

    def test_delete_model_success_serialization(self):
        # Mocks
        body = {"name": "121212"}
        # process
        error, data = AdminSerializer.delete_model(body)
        # asserts
        assert error == {}
        assert data == {"name": "121212"}
