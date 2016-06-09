from StreamDriver import StreamDriver
from Services.Service import *
from Models.Models import *
import time, sys, itertools
import argparse

# ARG PARSER
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument('-s', '--sleep', default=180)
parser.add_argument('-l', '--limit', default=10)
parser.add_argument('-e', '--env', default="production")
args = parser.parse_args()
# END ARG PARSER

# ENVIRONMENT DESTINATION - production || local || same
if args.env == "local":
    dest = "/Applications/MAMP/htdocs/pad-laravel/public/234c12f14-streams"
elif args.env == "same":
    dest = "streams.json"
else:
    dest = "/var/www/vhosts/pvpallday.com/laravel/public/234c12f13-streams/streams.json"
# END ENVIRONEMNT DESTINATION

# SPINNER
spinner = itertools.cycle(['-', '/', '|', '\\'])
# END SPINNER

# INTRO
print("%s"  % time.strftime("%c"), ">>> By: Dak Washbrook")
print("%s"  % time.strftime("%c"), ">>> Version: v0.1 BETA")
print("%s"  % time.strftime("%c"), ">>> Vinlock is awesome!")
print("%s"  % time.strftime("%c"), ">>> Starting Stream JSON Creator...")
# END INTRO

# SET SLEEP
try:
    seconds_to_sleep = int(args.sleep)
except TypeError:
    print("%s" % time.strftime("%c"), ">>> Invalid Seconds Input")
    seconds_to_sleep = 180

print("%s"  % time.strftime("%c"), ">>> Will Sleep for", seconds_to_sleep)

# END SET SLEEP

# SERVICE PROVIDERS
service_providers = {
    "twitch": TwitchService,
    "hitbox": HitboxService
}
print("%s"  % time.strftime("%c"), ">>> Service Providers Established...")
# END SERVICE PROVIDERS

# DRIVER LIMIT
try:
    driver_limit = int(args.limit)
except TypeError:
    print("%s" % time.strftime("%c"), ">>> Invalid Limit Amount")
    driver_limit = 10

# Set the limit for the game lists to 10
StreamDriver.set_limit(driver_limit)
print("%s"  % time.strftime("%c"), ">>> Driver Limit Set to 10...")
# END DRIVER LIMIT

while(True):
    import settings
    print("%s"  % time.strftime("%c"), ">>> Reconstructing JSON...")

    roles = Role.where('name', '=', 'supported').first()
    print("Obtained Supported Role...", end='\r')
    users = roles.users().get()
    print("Obtained Users in Supported Role...", end='\r')
    supported_list = {'twitch': [], "hitbox": []}

    print("Filling Custom Fields for Users...", next(spinner), end='\r')
    for user in users:
        print("Filling Custom Fields for Users...", next(spinner), end='\r')
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
    print("%s"  % time.strftime("%c"), ">>> Filled Custom Fields for Users.")

    supported_streams = []

    print("Building Stream Objects for Supported Streams...", next(spinner), end='\r')
    for service, streams in supported_list.items():
        print("Building Stream Objects for Supported Streams...", next(spinner), end='\r')
        all_supported = service_providers[service](StreamDriver.list_from_key(supported_list[service], 'username'))
        if all_supported.num_streams() > 0:
            for stream_object in all_supported.get():
                print("Building Stream Objects for Supported Streams...", next(spinner), end='\r')
                stream_object.set_custom('type', 'supported')
                for element in streams:
                    print("Building Stream Objects for Supported Streams...", next(spinner), end='\r')
                    if element['username'] == stream_object.username():
                        stream_object.set_custom('youtube', element['youtube'])
                        stream_object.set_custom('facebook', element['facebook'])
                        stream_object.set_custom('twitter', element['twitter'])
                        stream_object.set_custom('instagram', element['instagram'])
                        stream_object.set_custom('website', element['website'])
                        stream_object.set_custom('member_id', element['member_id'])
                supported_streams.append(stream_object)
    print("%s"  % time.strftime("%c"), ">>> Built Stream Objects for Supported Streams.")

    supported = Service(supported_streams)
    supported.sort()

    starter = Service([])

    print("Obtaining Active Games", next(spinner), end='\r')
    games = Game.where('status', '=', 1).get().pluck("name").all()
    for game in games:
        print("Obtaining Active Games", next(spinner), end='\r')
        starter.merge(TwitchService.game(game))
        starter.merge(HitboxService.game(game))
    print("%s"  % time.strftime("%c"), ">>> Obtained Active Games.")

    starter.sort()
    starter.set_all("type", "other")
    starter.set_all("youtube", None)
    starter.set_all("facebook", None)
    starter.set_all("twitter", None)
    starter.set_all("instagram", None)
    starter.set_all("website", None)
    starter.set_all("member_id", None)
    if supported.num_streams() > 0:
        starter.prepend(supported)
        starter.cut()
    else:
        starter.cut(9)

    if starter.output_to_json(dest):
        now = time.strftime("%c")
        print(">>> Generated JSON ---", "Current time %s"  % time.strftime("%c"))

    settings.db.disconnect()
    print("Sleeping for", seconds_to_sleep, "seconds... Night yo.")
    for i in range(seconds_to_sleep):
        time.sleep(1)
        print("", seconds_to_sleep-i, next(spinner), end='\r')
    # time.sleep(seconds_to_sleep)