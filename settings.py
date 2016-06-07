from os.path import join, dirname
from dotenv import load_dotenv
from orator import DatabaseManager, Model
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DRIVER = os.environ.get("DRIVER")
HOST = os.environ.get("HOST")
DATABASE = os.environ.get("DATABASE")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
PREFIX = os.environ.get("PREFIX")

config = {
    'mysql': {
        'driver': DRIVER,
        'host': HOST,
        'database': DATABASE,
        'user': USER,
        'password': PASSWORD,
        'prefix': PREFIX
    }
}

