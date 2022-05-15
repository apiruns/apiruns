from api.configs import app_configs
from api.serializers.types.cerberus import Cerberus


class Serializers:
    """Serializers allowed"""

    CERBERUS = "CERBERUS"


SERIALIZER_TYPES = {Serializers.CERBERUS: Cerberus}
Serializer = SERIALIZER_TYPES[app_configs.VALIDATOR_NAME]
