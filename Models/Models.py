from orator import Model
from orator.orm import has_one, belongs_to_many


class User(Model):
    __table__ = "pad_users"

    @has_one('user_id')
    def profile(self):
        return UserProfile

    @belongs_to_many('pad_role_user', 'user_id', 'role_id')
    def roles(self):
        return Role

    def primary_service(self):
        service = StreamService.find(self.profile.primary_service)
        return service.clean_name


class Game(Model):
    __table__ = "pad_games"


class Role(Model):
    __table__ = "pad_roles"

    @belongs_to_many('pad_role_user', 'role_id', 'user_id')
    def users(self):
        return User


class StreamService(Model):
    __table__ = "pad_stream_services"


class UserProfile(Model):
    __table__ = "pad_user_profiles"