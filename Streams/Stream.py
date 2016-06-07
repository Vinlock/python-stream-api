import abc, json, re, html, cgi

class Stream:
    __metaclass__ = abc.ABCMeta

    __guarded = [
        "username", "display_name", "preview", "status", "url", "viewers", "id", "avatar"
    ]

    _custom_members = {}

    def _stream(self):
        result = {
            "username": self.username(),
            "display_name": self.display_name(),
            "game": self.game(),
            "preview": {
                "small": self.small_preview(),
                "medium": self.medium_preview(),
                "large": self.large_preview()
            },
            "status": self.status(),
            "bio": self.bio(),
            "url": self.url(),
            "viewers": int(self.viewers()),
            "id": self.id(),
            "avatar": self.avatar(),
            "service": self._service,
            "followers": int(self.followers()),
            "created_at": self.created_at(),
            "updated_at": self.updated_at()
        }
        return result

    def set_custom(self, key, value):
        self._custom_members[key] = value

    def get(self):
        info = self._stream()
        custom_info = self._custom_members
        final = dict(info, **custom_info)
        return final

    def to_json(self):
        return json.dumps(self.get())

    @staticmethod
    def filter_bio(bio):
        bio = re.sub("/\r|\n/", "", html.unescape(cgi.escape(bio, True)))
        return bio

    def preview(self, size = "large"):
        switch = {
            "small": self.small_preview(),
            "medium": self.medium_preview(),
            "large": self.large_preview()
        }
        return switch.get(size, None)

    @abc.abstractmethod
    def username(self):
        """Stream Username"""
        return

    @abc.abstractmethod
    def display_name(self):
        """Stream Display Name"""
        return

    @abc.abstractmethod
    def game(self):
        """Stream Current Game"""
        return

    @abc.abstractmethod
    def large_preview(self):
        """Stream Large Preview Image"""
        return

    @abc.abstractmethod
    def medium_preview(self):
        """Stream Medium Preview Image"""
        return

    @abc.abstractmethod
    def small_preview(self):
        """Stream Small Preview Image"""
        return

    @abc.abstractmethod
    def status(self):
        """Stream Current Status/Title"""
        return

    @abc.abstractmethod
    def url(self):
        """Stream URL"""
        return

    @abc.abstractmethod
    def viewers(self):
        """Stream Amount of Viewers"""
        return

    @abc.abstractmethod
    def id(self):
        """Stream ID"""
        return

    @abc.abstractmethod
    def avatar(self):
        """Stream Avatar"""
        return

    @abc.abstractmethod
    def bio(self):
        """Stream Bio"""
        return

    @abc.abstractmethod
    def created_at(self):
        """Stream Started At/User Joined?"""
        return

    @abc.abstractmethod
    def updated_at(self):
        """Stream Updated At"""
        return

    @abc.abstractmethod
    def followers(self):
        """Stream Followers"""
        return