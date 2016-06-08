from Streams.Stream import Stream
import json, requests


class TwitchStream(Stream):
    _service = "twitch"

    STREAM_KEY = "streams"

    STREAM_API = "https://api.twitch.tv/kraken/streams?channel="

    GAMES_API = "https://api.twitch.tv/kraken/streams?game="

    USERS_API = "https://api.twitch.tv/kraken/users/"

    STREAM_URL = "http://www.twitch.tv/"

    DEFAULT_AVATAR = "http://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_150x150.png"

    def __init__(self, dictionary):
        self._stream_data = dictionary
        self._custom_members = {}

    def username(self):
        return self._stream_data['channel']['name']

    def display_name(self):
        return self._stream_data['channel']['display_name']

    def game(self):
        return self._stream_data['game']

    def large_preview(self):
        return self._stream_data['preview']['large']

    def medium_preview(self):
        return self._stream_data['preview']['medium']

    def small_preview(self):
        return self._stream_data['preview']['small']

    def status(self):
        return self._stream_data['channel']['status']

    def url(self):
        return self._stream_data['channel']['url']

    def viewers(self):
        return int(self._stream_data['viewers'])

    def id(self):
        return self._stream_data['channel']['_id']

    def avatar(self):
        avatar = self._stream_data['channel']['logo']
        if avatar is None:
            return self.DEFAULT_AVATAR
        else:
            return avatar

    def bio(self):
        request = requests.get(self.USERS_API+self.username())
        response = request.json()
        dictionary = json.dumps(response['bio'])
        return Stream.filter_bio(dictionary)

    def created_at(self):
        return self._stream_data['created_at']

    def updated_at(self):
        return self._stream_data['channel']['updated_at']

    def followers(self):
        return self._stream_data['channel']['followers']

