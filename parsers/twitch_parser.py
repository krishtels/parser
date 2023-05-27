import requests
from config.config import twitch_settings
from dao.kafka_dao import KafkaSetup
from di.twitch_di import TwitchService


class TwitchParser:
    def __init__(self, kafka: KafkaSetup, twitch_db: TwitchService):
        self.auth_url = "https://id.twitch.tv/oauth2/token"
        self.streams_url = "https://api.twitch.tv/helix/streams?first=10"
        self.kafka = kafka
        self.twitch_db = twitch_db.dao

    def auth(self, url):
        data = {
            "client_id": twitch_settings.TWITCH_CLIENT_ID,
            "client_secret": twitch_settings.TWITCH_SECRET_KEY,
            "grant_type": "client_credentials",
        }
        res = requests.post(url, data)

        return res.json()["access_token"]

    async def get_streams(self):
        token = self.auth(self.auth_url)
        res = requests.get(
            self.streams_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Client-Id": twitch_settings.TWITCH_CLIENT_ID,
            },
        )
        for stream in res.json()["data"]:
            stream_data = {
                "user_login": stream["user_login"],
                "game_name": stream["game_name"],
                "type": stream["type"],
                "title": stream["title"],
                "viewer_count": stream["viewer_count"],
                "language": stream["language"],
                "is_mature": stream["is_mature"],
            }
            self.kafka.producer.send("twitch", value=stream_data)
        await self.twitch_db.send_data(self.kafka.consumer_twitch)
