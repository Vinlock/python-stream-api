from StreamDriver import StreamDriver
from Models.Game import Game
from Models.UserProfile import UserProfile
from Models.StreamService import StreamService
from Models.User import User

# Set the limit for the game lists to 10
StreamDriver.set_limit(10)

users = User.where('profile.twitch', '!=', '').where('profile.hitbox', '!=', '').chunk(StreamDriver.NUM_PER_MULTI)

print(users)