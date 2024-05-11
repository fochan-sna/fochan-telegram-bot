from uuid import UUID
from dataclasses import dataclass

UserID = UUID
TopicID = UUID
MessageID = int


@dataclass
class User:
    id: UserID
    username: str


@dataclass
class Topic:
    id: TopicID
    name: str
    description: str


@dataclass
class Message:
    id: MessageID
    topic_id: TopicID
    user: User
    content: str