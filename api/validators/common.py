import uuid
from typing import Any
from typing import List
from typing import Tuple

from api.configs import app_configs


class AdminSerializerSchema:
    """Admin Serializer Schema."""

    @property
    def methods(self):
        """Get method avaibles.

        Returns:
            dict: methods.
        """
        return {
            "path": self.serialize_path,
            "model": self.serialize_model,
            "schema": self.serialize_schema,
        }

    def serialize(self, body: dict) -> Tuple[List[dict], dict]:
        """Serialize body.

        Args:
            body (dict): Body data.

        Returns:
            Tuple[dict, dict]: errors, body serialized.
        """
        new_body = {}
        errors = []
        new_body[app_configs.IDENTIFIER_ID] = str(uuid.uuid4())
        for key, method in self.methods.items():
            error, value = method(body.get(key))
            if error:
                errors.append(error)
                continue

            new_body[key] = value

        new_body["schema"] = body.get("schema")
        return errors, new_body

    def serialize_schema(self, value) -> Tuple[dict, Any]:
        """Serialize and validate schema field.

        Args:
            value (dict): schema.

        Returns:
            Tuple[dict, Any]: errors and schema.
        """
        error = {"schema": "schema is type object and not empty."}
        if not value:
            return error, value

        return {}, value

    def serialize_path(self, value) -> Tuple[dict, Any]:
        """Serialize and validate path field.

        Args:
            value (dict): path field.

        Returns:
            Tuple[dict, Any]: errors and path serialized.
        """
        error = {}
        if not value.startswith("/"):
            error["path"] = "the path must start with the '/' character."
            return error, value

        if value == "/":
            return {}, value

        # TODO: validate with path regex
        rf = filter(lambda x: not (x.isalpha() or x == ""), value.split("/"))
        if len(list(rf)):
            error["path"] = "the path must only contain letters and the '/' character."
            return error, value

        path_modified = value[:-1] if value.endswith("/") else value
        if len(path_modified.split("/")) > app_configs.PATH_SECTION:
            error["path"] = (
                f"Only one path with a maximum of {app_configs.PATH_SECTION - 1} "
                "sections is allowed."
            )
        return error, value

    def serialize_model(self, value) -> Tuple[dict, Any]:
        """Serialize and validate path field.

        Args:
            value (dict): path field.

        Returns:
            Tuple[dict, Any]: errors and model name serialized.
        """
        error = {"model": "the model only allows letters without spaces."}
        if not value.isalpha():
            return error, value
        return {}, value


def string_isalpha(field, value, error):
    if not value.isalpha():
        error(field, "the model only allows letters without spaces.")


def is_path_valid(field, value, error):
    if not value.startswith("/"):
        error(field, "the path must start with the '/' character.")

    rf = filter(lambda x: not (x.isalpha() or x == ""), value.split("/"))
    if len(list(rf)):
        error(field, "the path must only contain letters and the '/' character.")

    path_modified = value[:-1] if value.endswith("/") else value
    if len(path_modified.split("/")) > app_configs.PATH_SECTION:
        error(
            field,
            (
                f"Only one path with a maximum of {app_configs.PATH_SECTION - 1} "
                "sections is allowed."
            ),
        )
