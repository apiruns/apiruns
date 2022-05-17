from typing import Any
from typing import Tuple

from dacite import from_dict

from api.datastructures import Model
from api.serializers import Serializer


class AdminSerializer(Serializer):
    """Admin Serializer"""

    @classmethod
    def validate_admin_model(cls, body: dict) -> Tuple[bool, Any]:
        """Validate admin model

        Args:
            body (dict): body request.

        Returns:
            Tuple[bool, Any]: is valid and errors or model.
        """
        valid, errors = cls.validate_model(body)
        if not valid:
            return False, errors

        model = from_dict(data_class=Model, data=body)
        return True, model

    @classmethod
    def validate_delete(cls, body: dict) -> Tuple[bool, Any]:
        """Validate delete model

        Args:
            body (dict): request body.

        Returns:
            Tuple[bool, Any]: is valid and errors.
        """
        return cls.validate_delete_model(body)
