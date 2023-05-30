from config.database import connect_db
from dao.twitch_dao import TwitchDao

from di.service_di import Service


class TwitchService(Service):
    def __init__(self):
        self.dao = TwitchDao(connect_db())
