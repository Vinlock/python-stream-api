from orator import Model, DatabaseManager
import settings

db = DatabaseManager(settings.config)
Model.set_connection_resolver(db)

class StreamService(Model):
    __table__ = "pad_stream_services"
    pass