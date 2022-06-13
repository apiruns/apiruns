import os

# Engine configs
ENGINE_URI_DEFAULT = "mongodb://0.0.0.0:27017/"
ENGINE_NAME = os.environ.get("ENGINE_NAME", "MONGO")
ENGINE_DB_NAME = os.environ.get("ENGINE_DB_NAME", "apiruns")
ENGINE_URI = os.environ.get("ENGINE_URI", ENGINE_URI_DEFAULT)

# Mongo
MONGO_TLS = bool(os.environ.get("MONGO_TLS", False))
MONGO_CAFILE = os.environ.get("MONGO_CAFILE", "")

ORIGINS_DEFAULT = [
    "http://localhost",
    "http://localhost:8080",
]
ORIGINS_PROD = os.environ.get("ORIGINS")
ORIGINS = ORIGINS_PROD.split(",") if ORIGINS_PROD else ORIGINS_DEFAULT

# Validator configs
VALIDATOR_NAME = "CERBERUS"

# Models
MODEL_ADMIN_NAME = "apiruns_models"
IDENTIFIER_ID = "public_id"

# Internal feature
FEATURE_INTERNAL_PATH = os.environ.get("FEATURE_INTERNAL_PATH", None)
