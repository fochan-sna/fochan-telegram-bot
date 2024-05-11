import sys
import asyncio
import logging
from os import getenv
from time import sleep
from threading import Thread
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode
from aiogram.filters import CommandStart, Command

from fochan import FochanAPI

load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()
bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)

fochan = FochanAPI()

users = {}


def process_messages():
    while True:
        for message in fochan.get_messages(5):
            for user in users:
                if not users[user]['current_topic']:
                    continue

                if users[user]['last_message_got'] < message.id:
                    bot.send_message(user, message.content)
                    users[user]['last_message_got'] = message.id
        sleep(1)


@dp.message(CommandStart())
async def start(message: Message) -> None:
    if message.from_user.id not in users:
        users[message.chat.id] = {
            'user': fochan.create_user(),
            'current_topic': None,
            'last_message_got': -1
        }

    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(Command('topics'))
async def list_topics(message: Message) -> None:
    await message.answer('\n\n'.join(
        f'{hbold(topic.name)} {hcode(topic.id[-4:])}\n'
        f'{topic.description}'
        for topic in fochan.get_topics()
    ))


@dp.message(Command('topic'))
async def enter_topic(message: Message) -> None:
    topic_alias = message.text.split()[1]
    users[message.chat.id]['current_topic'] = next(
        (topic for topic in fochan.get_topics()
         if topic.id[-4:] == topic_alias), None
    )

    if users[message.chat.id]['current_topic']:
        await message.answer(
            f'You have entered to '
            f'{hbold(users[message.chat.id]['current_topic'].name)} topic'
        )
        return

    await message.answer('Topic not found')


@dp.message(Command('exit'))
async def leave_topic(message: Message) -> None:
    users[message.chat.id]['current_topic'] = None
    users[message.chat.id]['last_message_got'] = -1
    await message.answer('You have exited from the topic')


@dp.message()
async def send_message_or_default(message: Message) -> None:
    if not users[message.chat.id]['current_topic']:
        await message.answer('Enter the topic to start messaging')
        return

    fochan.send_message(
        topic_id=users[message.chat.id]['current_topic'].id,
        user_id=users[message.chat.id]['user'].id,
        message=message.text
    )


async def main() -> None:
    Thread(target=process_messages).start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
