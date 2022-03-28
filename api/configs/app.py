import os

# Engine configs
ENGINE_URI_DEFAULT = "mongodb://0.0.0.0:27017/"
ENGINE_NAME = os.environ.get("ENGINE_NAME", "MONGO")
ENGINE_DB_NAME = os.environ.get("ENGINE_DB_NAME", "apisrun")
ENGINE_URI = os.environ.get("ENGINE_URI", ENGINE_URI_DEFAULT)

# Validator configs
VALIDATOR_NAME = "CERBERUS"

# Models
MODEL_ADMIN_NAME = "apisrun_models"
IDENTIFIER_ID = "public_id"
QUERY_LIMIT = 50
PATH_SECTION = 7

# Features
INTERNALS = {
    "AUTHX": {
        "ON": os.environ.get("AUTHX", False),
        "JWT_SECRET": os.environ.get("AUTHX_JWT_SECRET"),
        "JWT_EXP": os.environ.get("AUTHX_JWT_EXP"),
        "JWT_ALGORITHM": "HS256",
        "MODEL": "apisrun_users",
        "SIGN_IN_PATH": "/admin/users/signin",
        "REGISTER_PATH": "/admin/users",
    }
}
