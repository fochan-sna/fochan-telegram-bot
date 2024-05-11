from requests import Session

from .types import *


class FochanAPI:
    def __init__(self):
        self.http = Session()

    def get_topics(self) -> list[Topic]:
        pass

    def get_messages(self, topic_id: TopicID, limit: int = 3):
        pass

    def send_message(self, topic_id: TopicID, user_id: UserID, message: str):
        pass
