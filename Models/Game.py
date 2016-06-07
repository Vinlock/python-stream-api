from orator import Model, DatabaseManager
import settings

db = DatabaseManager(settings.config)
Model.set_connection_resolver(db)

class Game(Model):
    __table__ = "pad_games"
    pass