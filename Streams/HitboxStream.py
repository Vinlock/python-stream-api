from Streams.Stream import Stream
import cgi, html

class HitboxStream(Stream):

    _service = "hitbox"

    STREAM_KEY = "livestream"

    STREAM_API = "https://www.hitbox.tv/api/media/live/"

    GAMES_API = "https://api.hitbox.tv/media/live/list?game="

    STREAM_IMG = "http://edge.sf.hitbox.tv"

    STREAM_URL = "http://www.hitbox.tv/"

    def __init__(self, dictionary):
        self._stream_data = dictionary
        self._custom_members = {}

    def username(self):
        return self._stream_data['media_user_name']

    def game(self):
        return self._stream_data['category_name']

    def avatar(self):
        return self.STREAM_IMG+self._stream_data['channel']['user_logo']

    def created_at(self):
        return self._stream_data['media_date_added']

    def display_name(self):
        return self._stream_data['media_display_name']

    def bio(self):
        return ""

    def status(self):
        return Stream.filter_bio(self._stream_data['media_status'])

    def medium_preview(self):
        return self.STREAM_IMG + self._stream_data['media_thumbnail_large']

    def updated_at(self):
        return self._stream_data['media_live_since']

    def small_preview(self):
        return self.STREAM_IMG + self._stream_data['media_thumbnail']

    def followers(self):
        return self._stream_data['channel']['followers']

    def id(self):
        return self._stream_data['media_id']

    def viewers(self):
        return self._stream_data['media_views']

    def large_preview(self):
        return self.STREAM_IMG + self._stream_data['media_thumbnail_large']

    def url(self):
        return self._stream_data['channel']['channel_link']
