from api.serializers.base import Serializer


def upper():
    """Return lambda with upper string"""
    return lambda s: s.upper()


class TestSerializer:

    schema_one = {
        "path": {
            "type": "string",
            "required": True,
            "empty": False,
        },
        "name": {
            "type": "string",
            "maxlength": 70,
            "coerce": (str, upper()),
        },
    }
    schema_two = {
        "path": {
            "type": "string",
            "required": True,
            "empty": False,
        },
        "name": {
            "type": "string",
            "maxlength": 70,
        },
    }

    def _get_data(self) -> dict:
        return {"path": "/users", "name": "users"}

    def test_schema_is_valid(self):
        resp = Serializer._validate_schema(self.schema_one)
        assert resp is None

    def test_schema_is_invalid(self):
        resp = Serializer._validate_schema({"path": {"type": "error"}})
        assert resp is not None

    def test_serialize_data_with_errors(self):
        errors, data = Serializer._serialize(self.schema_one, {})
        assert data == {}
        assert errors == {"path": ["required field"]}

    def test_serialize_data_with_funtion(self):
        errors, data = Serializer._serialize(self.schema_one, self._get_data())
        assert data == {"name": "USERS", "path": "/users"}
        assert errors == {}

    def test_serialize_data_without_funtion(self):
        errors, data = Serializer._serialize(self.schema_two, self._get_data())
        assert data == {"name": "users", "path": "/users"}
        assert errors == {}

    def test_serialize_data_with_purge(self):
        errors, data = Serializer._serialize(
            self.schema_one,
            {"name": "users", "path": "/users", "other": "true"},
            purge=True,
        )
        assert data == {"name": "USERS", "path": "/users"}
        assert errors == {}
