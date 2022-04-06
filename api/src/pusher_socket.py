import pusher
import json

from api.src.configuration import Configuration


class PusherSocket:
    def __init__(self, channel):
        self.channel = channel

        self.pusher_client = pusher.Pusher(
            app_id=Configuration.get("PUSHER_APP_ID"),
            key=Configuration.get("PUSHER_KEY"),
            secret=Configuration.get("PUSHER_SECRET"),
            cluster='eu',
            ssl=True
        )

    def send_notification(self, event_name, data):
        self.pusher_client.trigger(self.channel, event_name, data)
