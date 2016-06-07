from orator import Model
import settings

Model.set_connection_resolver(settings.db)

class StreamService(Model):
    __table__ = "pad_stream_services"
    pass