import configparser
from orator import DatabaseManager, Model

config = configparser.ConfigParser()

config.read('config.ini')


config = {
    'mysql': {
        'driver': config['database']['driver'],
        'host': config['database']['host'],
        'database': config['database']['database'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'prefix': config['database']['prefix']
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)