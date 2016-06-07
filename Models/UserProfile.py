from orator import Model, DatabaseManager
import settings

db = DatabaseManager(settings.config)
Model.set_connection_resolver(db)


class UserProfile(Model):
    __table__ = "pad_user_profiles"
    pass