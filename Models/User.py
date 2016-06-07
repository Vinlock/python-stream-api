from orator import Model, DatabaseManager
from orator.orm import has_one
from Models.UserProfile import UserProfile
import settings

db = DatabaseManager(settings.config)
Model.set_connection_resolver(db)

class User(Model):
    __table__ = "pad_users"

    @has_one('user_id')
    def profile(self):
        return UserProfile