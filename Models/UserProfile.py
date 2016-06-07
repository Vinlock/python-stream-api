from orator import Model
import settings

Model.set_connection_resolver(settings.db)


class UserProfile(Model):
    __table__ = "pad_user_profiles"
    pass