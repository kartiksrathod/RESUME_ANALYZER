import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env in the repository root.
env_path = Path(__file__).resolve().parent / '.env'
if env_path.exists():
    load_dotenv(env_path)


def get_db_connection():
    return mysql.connector.connect(
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'password'),
        host=os.getenv('DB_HOST', '127.0.0.1'),
        database=os.getenv('DB_NAME', 'resumes'),
        auth_plugin=os.getenv('DB_AUTH_PLUGIN', 'mysql_native_password'),
    )
