import configparser
from orator import Model
from orator_cache import DatabaseManager, Cache

config = configparser.ConfigParser()

config.read('config.ini')


db_config = {
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
            'host': config['redis']['host'],
            'password': config['redis']['password'],
            'port': config['redis']['port'],
            'db': 0
        }
    }
}

twitch = {
    'clientid': config['twitch']['clientid']
}

cache = Cache(stores)

db = DatabaseManager(db_config, cache=cache)
Model.set_connection_resolver(db)