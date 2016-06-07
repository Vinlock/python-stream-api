from Streams.Stream import Stream
from StreamDriver import StreamDriver
import json


class Service:
    _service = None

    _streams = []

    def __init__(self, **kwargs):
        streams = kwargs.get('streams', None)
        self._service = kwargs.get('service', None)
        if isinstance(streams, list):
            self._streams = self._streams + streams
        elif isinstance(streams, Stream):
            self._streams.append(streams)

    # Get Streams Methods
    def get(self):
        return self._streams

    def get_json(self):
        return json.dumps(self.get())

    @classmethod
    def game(cls, games):
        if isinstance(games, list):
            new_list = []
            for game in games:
                new_list = new_list + StreamDriver.by_game(game, cls._service)
        elif isinstance(games, str):
            return StreamDriver.by_game(games, cls._service)

    @classmethod
    def streams(cls, streams):
        if isinstance(streams, list):
            return StreamDriver.get_streams(streams, cls._service)
        elif isinstance(streams, str):
            return StreamDriver.get_streams([streams], cls._service)

    # Merge Service Objects
    def merge(self, service_object):
        self._streams = self._streams + service_object._streams

    def sort(self, **kwargs):
        sort_key = kwargs.get('sort_key', None)
        order = kwargs.get('order', None)

        if sort_key is None:
            sort_key = 'viewers'

        if order is None:
            order = "desc"

        if order is "asc":
            reversed = False
        else:
            reversed = True

        self._streams = sorted(all, key=lambda k: k[sort_key], reverse=reversed)

    def output_to_json(self, file="streams.json"):
        with open(file, 'w') as streams_file:
            json.dump(self._streams, streams_file)



