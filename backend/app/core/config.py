import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret

API_V1_STR = "/api/v1"

load_dotenv(".env")

PROJECT_NAME = os.getenv("PROJECT_NAME", "FastAPI example application")


BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS"
)  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://local.dockertoolbox.tiangolo.com"

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASS = os.getenv("MONGO_PASS", "pass")
MONGO_DEFAULT_DB = os.getenv("MONGO_DEFAULT_DB", "fastapi")
MONGO_FS_DB = os.getenv("MONGO_FS_DB", "fs")
# MONGO_DB = os.getenv("MONGO_DB", "fastapi")


# MONGODB_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"