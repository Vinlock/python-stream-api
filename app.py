from StreamDriver import StreamDriver
from Services.Service import *
from Models.Models import *
import time, sys, itertools
import argparse


class App(object):
    def __init__(self):
        # STARTUP
        self.__console("By: Dak Washbrook")
        self.__console("Version: v0.1 BETA")
        self.__console("Vinlock is awesome!")
        self.__console("Starting Stream JSON Creator...")

        # SPINNER
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])

        # APP ARGUMENTS
        self.args = self.__parse_args()

        # APP SLEEP TIME
        self.sleep = self.__sleep()

        # APP SERVICE PROVIDERS
        self.service_providers = self.__providers()

        # APP STREAM DRIVER LIMIT
        self.limit = self.__limit()

        # APP ENVIRONEMNT
        self.env = self.args.env

    def __sleep(self):
        try:
            sleep = int(self.args.sleep)
        except TypeError:
            self.__console("Invalid Sleep Seconds.")
            sleep = 180
        self.__console("Will sleep for " + str(sleep) + " seconds.")
        return sleep

    def __limit(self):
        try:
            limit = int(self.args.limit)
        except TypeError:
            self.__console("Invalid Limit Amount.")
            limit = 10
        StreamDriver.set_limit(limit)
        self.__console("Stream Driver Limit set to " + str(limit))
        return limit

    def __providers(self):
        providers = {
            "twitch": TwitchService,
            "hitbox": HitboxService
        }
        self.__console("Service Providers Established...")
        return providers

    def __console(self, string):
        print("%s" % time.strftime("%c"), ">>> "+string)

    def __cnsltemp(self, string, spinner=True):
        if spinner:
            print(string, next(self.spinner), end='\r')
        else:
            print(string, end='\r')

    def __parse_args(self):
        parser = argparse.ArgumentParser(description="Parser")
        parser.add_argument('-s', '--sleep', default=180)
        parser.add_argument('-l', '--limit', default=10)
        parser.add_argument('-e', '--env', default="production")
        return parser.parse_args()

    def __output(self):
        if self.env == "local":
            dest = "/Applications/MAMP/htdocs/pad-laravel/public/234c12f14-streams/streams.json"
        elif self.env == "same":
            dest = "streams.json"
        else:
            dest = "/var/www/vhosts/pvpallday.com/laravel/public/234c12f14-streams/streams.json"
        return dest

    def __get_supported(self):
        roles = Role.where('name', '=', 'supported').first()
        self.__cnsltemp("Obtained Supported Role...")
        users = roles.users().get()
        self.__cnsltemp("Obtained Users in Supported Role...")
        return users

    def __fill_custom_fields(self, users):
        supported_list = {'twitch': [], 'hitbox': []}
        for user in users:
            self.__cnsltemp("Filling Custom Fields for Users...")
            service = user.primary_service()
            username = getattr(user.profile, service)
            stream_info = {
                'username': username,
                'youtube': user.profile.youtube,
                'facebook': user.profile.facebook,
                'twitter': user.profile.twitter,
                'instagram': user.profile.instagram,
                'website': user.profile.website,
                'member_id': user.profile.user_id
            }
            if username and service:
                supported_list[service].append(stream_info)
            self.__console("Filled Custom Fields for Users")
        return supported_list

    def __build_streams(self, users):
        def status():
            self.__cnsltemp("Building Stream Objects for Supported Streams...")
        supported_streams = []
        supported_list = self.__fill_custom_fields(users)
        status()
        for service, streams in supported_list.items():
            status()
            all_supported = self.service_providers[service](StreamDriver.list_from_key(supported_list[service], 'username'))
            if all_supported.num_streams() > 0:
                for stream_object in all_supported.get():
                    status()
                    stream_object.set_custom('type', 'supported')
                    for element in streams:
                        status()
                        if element['username'] == stream_object.username():
                            stream_object.set_custom('youtube', element['youtube'])
                            stream_object.set_custom('facebook', element['facebook'])
                            stream_object.set_custom('twitter', element['twitter'])
                            stream_object.set_custom('instagram', element['instagram'])
                            stream_object.set_custom('website', element['website'])
                            stream_object.set_custom('member_id', element['member_id'])
                    supported_streams.append(stream_object)
        self.__console("Built Stream Objects for Supported Streams")
        return supported_streams

    def __active_games(self):
        starter = None
        def status():
            self.__cnsltemp("Obtaining Active Games")
        games = Game.where('status', '=', 1).get().pluck('name').all()
        for game in games:
            status()
            if starter is None:
                starter = TwitchService.game(game)
            else:
                starter.merge(TwitchService.game(game))
            if starter is None:
                starter = HitboxService.game(game)
            else:
                starter.merge(HitboxService.game(game))
        self.__console("Obtained Active Games")
        starter.sort()
        starter.set_all("type", "other")
        starter.set_all("youtube", None)
        starter.set_all("facebook", None)
        starter.set_all("twitter", None)
        starter.set_all("instagram", None)
        starter.set_all("website", None)
        starter.set_all("member_id", None)
        return starter

    def __gotosleep(self):
        for i in range(self.sleep):
            time.sleep(1)
            self.__cnsltemp(" "+str(self.sleep-i))



    def run(self):
        while True:
            import settings
            self.__console("Reconstructing JSON...")

            # Get all supported users.
            users = self.__get_supported()

            # Build their streams from the Users found.
            supported_streams = self.__build_streams(users)

            # Create Service Objects from the streams found.
            supported = Service(supported_streams)
            # Sort them by viewers highest to lowest.
            supported.sort()

            # Find all other streams that are streaming the supported Games.
            others = self.__active_games()

            # If there are supported streamers online...
            if supported.num_streams() > 0:
                # Prepend Supported to Active Game Streamers
                others.prepend(supported)
                # Make sure the correct amount of streamers are kept, the others are cut.
                others.cut()
            else:
                others.cut(9)

            # Output to JSON.
            if others.output_to_json(self.__output()):
                self.__console("Generated JSON. DONE")

            # Disconnect to DB, will reconnect on next run.
            settings.db.disconnect()
            self.__console("Sleeping For " + str(self.sleep) + " seconds... Night yo.")
            # Sleep
            self.__gotosleep()

app = App()
app.run()
# while True:
#     try:
#         app.run()
#     except KeyboardInterrupt:
#         raise KeyboardInterrupt
#     except:
#         continue
