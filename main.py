import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    report = leak_osint.request([message.text])[0]

    await message.answer('\n\n'.join(
        f'<b>{db_name}</b>\n' + '\n'.join(
            '\n'.join(
                [f'├ {field} - {value}' for field, value in list(block.items())[:-1]] +
                [f'└ {list(block.keys())[-1]} - {list(block.values())[-1]}']
            ) for block in data['Data']
        ) for db_name, data in report.items()
    ))


async def main() -> None:
    bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
