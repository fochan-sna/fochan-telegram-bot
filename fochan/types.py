from uuid import UUID
from dataclasses import dataclass

UserID = UUID
TopicID = UUID
MessageID = UUID


@dataclass
class Message:
    id: MessageID
    topic_id: TopicID
    user_id: UserID
    content: str
    sent_at: int


@dataclass
class Topic:
    id: UUID
    name: str
    description: str


@dataclass
class User:
    id: UserID
    username: str
