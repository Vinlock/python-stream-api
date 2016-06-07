import configparser
from orator import Model
from orator_cache import DatabaseManager, Cache

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

stores = {
    'stores': {
        'redis': {
            'driver': 'redis',
            'host': 'localhost',
            'password': 'aw45gbnb3w4b4w',
            'port': 6379,
            'db': 0
        }
    }
}

cache = Cache(stores)

db = DatabaseManager(config, cache=cache)
Model.set_connection_resolver(db)