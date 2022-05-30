import os

# Engine configs
ENGINE_URI_DEFAULT = "mongodb://0.0.0.0:27017/"
ENGINE_NAME = os.environ.get("ENGINE_NAME", "MONGO")
ENGINE_DB_NAME = os.environ.get("ENGINE_DB_NAME", "apisrun")
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
MODEL_ADMIN_NAME = "apisrun_models"
IDENTIFIER_ID = "public_id"
QUERY_LIMIT = 50
PATH_SECTION = 7

# Features
INTERNALS = {
    "MICRO": {
        "ON": bool(os.environ.get("MICRO", False)),
        "JWT_SECRET": os.environ.get("MICRO_JWT_SECRET", "SUPER_SECRET"),
        "JWT_EXP": int(os.environ.get("MICRO_JWT_EXP", 3600)),
        "JWT_ALGORITHM": "HS256",
        "MODEL": MODEL_ADMIN_NAME,
        "MODEL_ROWS": "apisrun_rows",
        "SIGN_IN_PATH": "/admin/users/signin",
        "REGISTER_PATH": "/admin/users",
        "ALLOWED_MODELS": int(os.environ.get("MICRO_ALLOWED_MODELS", 10)),
        "USER_MODEL": "apisrun_users",
    }
}
