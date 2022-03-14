from api.configs import app_configs
from api.validators.cerberus import Cerberus


VALIDATOR_TYPES = {"CERBERUS": Cerberus}

validate = VALIDATOR_TYPES[app_configs.VALIDATOR_NAME]
