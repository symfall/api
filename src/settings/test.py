import os

DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "example")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "example")
DB_DRIVER = os.environ.get("DB_DRIVER", "postgresql")
DB_URL = "{}://{}:{}@{}/{}".format(DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
