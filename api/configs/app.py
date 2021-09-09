import os

ENGINE_NAME = os.environ.get("ENGINE_NAME", "MONGO")
ENGINE_DB_NAME = os.environ.get("ENGINE_NAME", "apisrun")
ENGINE_URI_DEFAULT = "mongodb://root:password@0.0.0.0:27017/"
ENGINE_URI = os.environ.get("ENGINE_URI", ENGINE_URI_DEFAULT)

VALIDATOR_NAME = "CERBERUS"

QUERY_LIMIT = 10
PATH_SECTION = 7
