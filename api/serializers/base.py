from typing import Tuple
from typing import Union

from cerberus import Validator
from cerberus.schema import SchemaError


class Serializer:
    """Base Serializer based in Cerberus"""

    @classmethod
    def _validate_schema(cls, schema: dict) -> Union[None, dict]:
        """Validate if cerberus schema is valid.

        Args:
            schema (dict): Cerberus schema.

        Returns:
            Union[None, dict]: None if is valid else validation errors.
        """
        try:
            Validator(schema)
            return None
        except SchemaError as e:
            return e.args[0]

    @classmethod
    def _serialize(
        cls, schema: dict, data: Union[dict, list], purge: bool = False
    ) -> Tuple[dict, Union[dict, list]]:
        """Serialize data.

        Args:
            schema (dict): Cerberus schema.
            data (Union[dict, list]): Data to serialize.
            purge (bool, optional): Purge unknown field. Defaults to False.

        Returns:
            Tuple[dict, Union[dict, list]]: Returns errors and data serialized.
        """
        v = Validator(schema, purge_unknown=purge)
        v.normalized(data)
        v.validate(v.document)
        return v.errors, v.document
