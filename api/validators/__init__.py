from api.validators.cerberus import CerberusValidator
from api import configs


VALIDATOR_TYPES = {
    "CERBERUS": CerberusValidator
}

validate = VALIDATOR_TYPES[configs.VALIDATOR_NAME]
