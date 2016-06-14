from Streams.TwitchStream import TwitchStream
from Streams.HitboxStream import HitboxStream
import abc, requests, urllib.parse, time, simplejson


class StreamDriver:
    __metaclass__ = abc.ABCMeta

    NUM_PER_MULTI = 100

    _limit = 0

    providers = {
        "twitch": TwitchStream,
        "hitbox": HitboxStream
    }

    @staticmethod
    def get_streams(usernames, service):
        streams = []

        chunks = StreamDriver.chunks(usernames, StreamDriver.NUM_PER_MULTI)

        for chunk in chunks:
            list = ",".join(chunk)
            while True:
                try:
                    data = requests.get(StreamDriver.providers[service].STREAM_API+list).json()
                except ConnectionError:
                    StreamDriver.iferror(300)
                    continue
                except ValueError:
                    return []
                break
            for stream in data[StreamDriver.providers[service].STREAM_KEY]:
                stream_object = StreamDriver.providers[service](stream)
                streams.append(stream_object)
        return streams

    @staticmethod
    def iferror(sleep):
        print("%s" % time.strftime("%c"), ">>> " + "Request Connection Error Occurred. Sleeping for "+sleep+" seconds then trying again.")
        time.sleep(sleep)

    @staticmethod
    def by_game(game, service):
        if StreamDriver._limit is 0:
            limit = StreamDriver.NUM_PER_MULTI
        else:
            limit = StreamDriver._limit

        streams = []

        game = urllib.parse.quote(game)
        stream_key = StreamDriver.providers[service].STREAM_KEY
        while True:
            try:
                data = requests.get(StreamDriver.providers[service].GAMES_API+game+"&limit="+str(limit)).json()
            except ConnectionError:
                StreamDriver.iferror(100)
                continue
            except ValueError:
                return []
            break
        if stream_key in data:
            for stream in data[stream_key]:
                stream_object = StreamDriver.providers[service](stream)
                streams.append(stream_object)
        return streams

    @staticmethod
    def set_limit(int):
        StreamDriver._limit = int

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @staticmethod
    def list_from_key(array, key):
        new_list = []
        for single in array:
            new_list.append(single[key])
        return new_list
