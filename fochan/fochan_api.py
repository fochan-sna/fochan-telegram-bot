from requests import Session
from datetime import datetime

from .types import *
from .const import *


class FochanAPI:
    def __init__(self):
        self.http = Session()

    def create_user(self) -> User:
        return User(
            **self.http.get(FOCHAN_API_CREATE_USER_URL).json()
        )

    def get_topics(self) -> list[Topic]:
        return [Topic(**topic)
                for topic in self.http.get(FOCHAN_API_GET_TOPICS_URL).json()['topics']]

    def get_messages(self, limit: int = 3) -> list[Message]:
        return [Message(message_id=message['message_id'],
                        topic_id=message['topic_id'],
                        user=User(**message['user']),
                        content=message['content'],
                        sent_at=datetime.strptime(message['sent_at'], "%Y-%m-%dT%H:%M:%S.%f").timestamp())
                for message in self.http.get(FOCHAN_API_GET_MESSAGES_URL,
                                             params={'limit': limit}).json()['messages']]

    def send_message(self, topic_id: TopicID, user_id: UserID, message: str) -> None:
        self.http.post(FOCHAN_API_SEND_MESSAGE_URL,
                       json={'topic_id': topic_id,
                             'user_id': user_id,
                             'message': message})
