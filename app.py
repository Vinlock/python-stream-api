import settings # To Activate Database Connection
from StreamDriver import StreamDriver
from Services.Service import *
from Models.Models import *
import time
import sys

args = sys.argv

service_providers = {
    "twitch": TwitchService,
    "hitbox": HitboxService
}

# Set the limit for the game lists to 10
StreamDriver.set_limit(10)

while(True):

    roles = Role.where('name', '=', 'supported').first()

    users = roles.users().get()

    supported_list = {'twitch': [], "hitbox": []}

    for user in users:
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

    supported_streams = []

    for service, streams in supported_list.items():
        all_supported = service_providers[service](StreamDriver.list_from_key(supported_list[service], 'username'))
        if all_supported.num_streams() > 0:
            for stream_object in all_supported.get():
                stream_object.set_custom('type', 'supported')
                for element in streams:
                    if element['username'] == stream_object.username():
                        stream_object.set_custom('youtube', element['youtube'])
                        stream_object.set_custom('facebook', element['facebook'])
                        stream_object.set_custom('twitter', element['twitter'])
                        stream_object.set_custom('instagram', element['instagram'])
                        stream_object.set_custom('website', element['website'])
                        stream_object.set_custom('member_id', element['member_id'])
                supported_streams.append(stream_object)

    supported = Service(supported_streams)
    supported.sort()

    starter = Service([])
    games = Game.where('status', '=', 1).get().pluck("name").all()
    for game in games:
        starter.merge(TwitchService.game(game))
        starter.merge(HitboxService.game(game))

    starter.sort()
    starter.set_all("type", "other")
    starter.set_all("youtube", None)
    starter.set_all("facebook", None)
    starter.set_all("twitter", None)
    starter.set_all("instagram", None)
    starter.set_all("website", None)
    starter.set_all("member_id", None)
    starter.prepend(supported)
    starter.cut()
    if starter.output_to_json():
        now = time.strftime("%c")
        print(">>> Generated JSON", "Current time %s"  % now)
    if (len(args) > 1):
        try:
            val = int(args[1])
            seconds_to_sleep = val
        except TypeError:
            seconds_to_sleep = 180
    else:
        seconds_to_sleep = 180

    print("Sleeping for", seconds_to_sleep)
    time.sleep(seconds_to_sleep)