import sys
import asyncio
import logging
from time import time
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties

from fochan import FochanAPI

load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()
bot = Bot(TELEGRAM_BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

fochan = FochanAPI()

users = {}


async def process_messages():
    for message in fochan.get_messages(5):
        for user in users:
            if (users[user]['current_topic'] and
                    users[user]['current_topic'].topic_id == message.topic_id and
                    users[user]['last_message_got'] < message.message_id and
                    users[user]['user'].user_id != message.user.user_id):
                await bot.send_message(user, f'[{hbold(message.user.username)}]\n'
                                             f'{message.content}')
                users[user]['last_message_got'] = message.message_id


async def register_user(tg_user_id: int):
    if tg_user_id not in users:
        users[tg_user_id] = {
            'user': fochan.create_user(),
            'current_topic': None,
            'last_message_got': fochan.get_messages(1)[0].message_id
        }


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await register_user(message.chat.id)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(Command('topics'))
async def list_topics(message: Message) -> None:
    await register_user(message.chat.id)
    await message.answer('\n\n'.join(
        f'{hbold(topic.name)} {hcode(topic.topic_id[-4:])}\n'
        f'{topic.description}'
        for topic in fochan.get_topics())
    )


@dp.message(Command('topic'))
async def enter_topic(message: Message) -> None:
    await register_user(message.chat.id)

    if len(message.text.split()) != 2:
        await message.answer('Send <code>/topic <topic id></code>')

    topic_alias = message.text.split()[1]
    users[message.chat.id]['current_topic'] = next(
        (topic for topic in fochan.get_topics()
         if topic.topic_id[-4:] == topic_alias), None
    )

    if users[message.chat.id]['current_topic']:
        await message.answer(
            f'You have entered to '
            f'{hbold(users[message.chat.id]["current_topic"].name)} topic'
        )
        return

    await message.answer('Topic not found')


@dp.message(Command('exit'))
async def leave_topic(message: Message) -> None:
    await register_user(message.chat.id)

    users[message.chat.id]['current_topic'] = None
    users[message.chat.id]['last_message_got'] = -1
    await message.answer('You have exited from the topic')


@dp.message()
async def send_message_or_default(message: Message) -> None:
    await register_user(message.chat.id)

    if not users[message.chat.id]['current_topic']:
        await message.answer('Enter the topic to start messaging')
        return

    fochan.send_message(
        topic_id=users[message.chat.id]['current_topic'].topic_id,
        user_id=users[message.chat.id]['user'].user_id,
        message=message.text
    )

    await process_messages()


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
