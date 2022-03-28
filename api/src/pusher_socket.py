import pusher
import json


class PusherSocket:
    def __init__(self, channel):
        self.channel = channel

        with open("api/conf.json", "r") as config:
            data = json.load(config)

        self.pusher_client = pusher.Pusher(
            app_id=data["pusher_app_id"],
            key=data["pusher_key"],
            secret=data["pusher_secret"],
            cluster='eu',
            ssl=True
        )

    def send_notification(self, event_name, data):
        self.pusher_client.trigger(self.channel, event_name, data)
