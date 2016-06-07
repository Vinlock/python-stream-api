from Streams.Stream import Stream
from StreamDriver import StreamDriver
import json


class Service:
    _service = None

    _streams = []

    def __init__(self, streams):
        self._streams = streams

    # Get Streams Methods
    def get(self):
        return self._streams

    def get_dict(self):
        streams = []
        for stream in self._streams:
            streams.append(stream.get())
        return streams

    def get_json(self):
        return json.dumps(self.get_dict())

    def set_all(self, key, value):
        for stream in self._streams:
            stream.set_custom(key, value)

    def num_streams(self):
        return len(self._streams)

    @classmethod
    def game(cls, games):
        if isinstance(games, list):
            new_list = []
            for game in games:
                new_list = new_list + StreamDriver.by_game(game, cls._service)
            return Service(new_list)
        elif isinstance(games, str):
            return Service(StreamDriver.by_game(games, cls._service))

    @classmethod
    def streams(cls, streams):
        if isinstance(streams, list):
            return Service(StreamDriver.get_streams(streams, cls._service))
        elif isinstance(streams, str):
            return Service(StreamDriver.get_streams([streams], cls._service))

    # Merge Service Objects
    def merge(self, service_object):
        self._streams = self.get() + service_object.get()
        self.sort()

    def prepend(self, service_object):
        self.sort()
        service_object.sort()
        self._streams = service_object.get() + self.get()

    def cut(self, num=10):
        self._streams = self._streams[:num]

    def sort(self):
        self._streams = sorted(self._streams, key=lambda k: k.viewers(), reverse=True)

    def output_to_json(self, file="streams.json"):
        with open(file, 'w') as streams_file:
            json.dump(self.get_dict(), streams_file)
        return True


class TwitchService(Service):
    _service = "twitch"

    def __init__(self, streams):
        self._streams = self.streams(streams).get()


class HitboxService(Service):
    _service = "hitbox"

    def __init__(self, streams):
        self._streams = self.streams(streams).get()
