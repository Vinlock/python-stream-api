from orator import Model
from orator.orm import has_one
from Models.UserProfile import UserProfile


class User(Model):
    __table__ = "pad_users"

    @has_one('user_id')
    def profile(self):
        return UserProfile