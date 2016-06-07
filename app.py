from StreamDriver import StreamDriver
from Models.Game import Game
from Models.UserProfile import UserProfile
from Models.StreamService import StreamServices

# Set the limit for the game lists to 10
StreamDriver.set_limit(10)

profiles = UserProfile.where('twitch', '!=', '').where('hitbox', '!='.chunk(StreamDriver.NUM_PER_MULTI)

