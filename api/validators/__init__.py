from api.configs import app_configs
from api.validators.cerberus import CerberusValidator


VALIDATOR_TYPES = {"CERBERUS": CerberusValidator}

validate = VALIDATOR_TYPES[app_configs.VALIDATOR_NAME]
