import os

# Engine configs
ENGINE_URI_DEFAULT = "mongodb://0.0.0.0:27017/"
ENGINE_NAME = os.environ.get("ENGINE_NAME", "MONGO")
ENGINE_DB_NAME = os.environ.get("ENGINE_DB_NAME", "apisrun")
ENGINE_URI = os.environ.get("ENGINE_URI", ENGINE_URI_DEFAULT)

# Validator configs
VALIDATOR_NAME = "CERBERUS"

QUERY_LIMIT = 10
PATH_SECTION = 7

# Models
MODEL_ADMIN_NAME = "apisrun_models"
