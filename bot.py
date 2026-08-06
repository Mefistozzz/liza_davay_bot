import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PROXY = os.getenv("BOT_PROXY") or None
CHANNEL_USERNAME = "liza_davay_shodim"
CHANNEL_ID = f"@{CHANNEL_USERNAME}"
CHANNEL_URL = f"https://t.me/{CHANNEL_USERNAME}"

WELCOME_TEXT = (
    "Добро пожаловать!\n"
    "Для получения карты с локациями подпишитесь на канал и нажмите кнопку ниже 👇"
)

MAP_TEXT = (
    "Подборки моих любимых локаций Москвы в Яндекс Картах:\n\n"
    '📍 <a href="https://yandex.ru/maps/?bookmarks%5BpublicId%5D=7GUXDbw7">'
    "Классные бары</a>\n"
    '📍 <a href="https://yandex.ru/maps/?bookmarks%5BpublicId%5D=uEFKTT_A">'
    "Места для завтраков и бранчей</a>\n"
    '📍 <a href="https://yandex.ru/maps/?bookmarks%5BpublicId%5D=1tT7hv3O">'
    "Музеи Москвы и МО</a>\n"
    '📍 <a href="https://yandex.ru/maps/?bookmarks%5BpublicId%5D=eWetwLug">'
    "Рестораны</a>\n"
    '📍 <a href="https://yandex.ru/maps/?bookmarks%5BpublicId%5D=1Ppe-nky">'
    "Кафе, где можно вкусно поесть</a>\n"
    '📍 <a href="https://yandex.ru/maps/?bookmarks%5BpublicId%5D=H9IPV-8S">'
    "Места для прогулок</a>\n\n"
    "Спасибо, что присоединились! Карты будут постоянно пополняться "
    "новыми локациями."
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подписаться", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="Получить карту", callback_data="get_map")],
        ]
    )


async def is_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception as exc:
        logger.warning("Subscription check failed for user %s: %s", user_id, exc)
        return False


async def main() -> None:
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set. Copy .env.example to .env and add your token.")
        sys.exit(1)

    bot = Bot(
        token=BOT_TOKEN,
        session=AiohttpSession(proxy=BOT_PROXY) if BOT_PROXY else None,
    )
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: Message) -> None:
        await message.answer(WELCOME_TEXT, reply_markup=start_keyboard())

    @dp.callback_query(F.data == "get_map")
    async def get_map(callback: CallbackQuery) -> None:
        if not callback.from_user:
            await callback.answer()
            return

        if await is_subscribed(bot, callback.from_user.id):
            await callback.message.answer(MAP_TEXT)
            await callback.answer()
            return

        await callback.answer(
            "Сначала подпишитесь на канал и затем нажмите «Получить карту» снова.",
            show_alert=True,
        )

    logger.info("Bot @LizaDavay_Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
