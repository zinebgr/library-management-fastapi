import os
from dotenv import load_dotenv

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ENV_PATH = os.path.join(ROOT_PATH, '.env')

load_dotenv(ENV_PATH)

class Setting:
    db_user = os.environ.get('DB_USER', "root")
    db_pass = os.environ.get('DB_PASS', "")
    db_host = os.environ.get('DB_HOST', "localhost")
    db_name = os.environ.get('DB_NAME', "library_db")

setting = Setting()