from uuid import UUID
from dataclasses import dataclass

UserID = UUID
TopicID = UUID
MessageID = int


@dataclass
class User:
    user_id: UserID
    username: str


@dataclass
class Topic:
    topic_id: TopicID
    name: str
    description: str


@dataclass
class Message:
    message_id: MessageID
    topic_id: TopicID
    user: User
    content: str
    sent_at: float
