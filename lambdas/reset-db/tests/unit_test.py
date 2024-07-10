import json
from scripts.app import lambda_handler
from scripts.app import get_db_connector

DUMMY_DB_HOSTNAME = "dummy_db_hostname"
DUMMY_DB_PORT = 3306
DUMMY_DB_REGION = "dummy_db_region"
DUMMY_DB_USERNAME = "XXXXXXXXXXXXXXXXX"
DUMMY_DB_PASSWORD = "XXXXXXXXXXXXXXXXX"
DUMMY_DB_NAME = "dummy_db_name"

def get_db_connector_creates_connection():
    assert get_db_connector(DUMMY_DB_HOSTNAME, DUMMY_DB_PORT, DUMMY_DB_REGION, DUMMY_DB_USERNAME, DUMMY_DB_PASSWORD, DUMMY_DB_NAME) is not None

 