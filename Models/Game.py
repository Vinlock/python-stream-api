from orator import Model
import settings

Model.set_connection_resolver(settings.db)

class Game(Model):
    __table__ = "pad_games"
    pass