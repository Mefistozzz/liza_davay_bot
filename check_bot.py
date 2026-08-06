import asyncio
import os
import sys

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PROXY = os.getenv("BOT_PROXY") or None
CHANNEL_ID = "@liza_davay_shodim"


async def main() -> None:
    if not BOT_TOKEN:
        print("FAIL: BOT_TOKEN is not set in .env")
        sys.exit(1)

    bot = Bot(
        token=BOT_TOKEN,
        session=AiohttpSession(proxy=BOT_PROXY) if BOT_PROXY else None,
    )

    try:
        me = await bot.get_me()
        print(f"OK: bot @{me.username} is reachable")

        chat = await bot.get_chat(CHANNEL_ID)
        print(f"OK: channel '{chat.title}' (@{chat.username}) is reachable")

        admins = await bot.get_chat_administrators(CHANNEL_ID)
        bot_is_admin = any(
            admin.user and admin.user.username and admin.user.username.lower() == me.username.lower()
            for admin in admins
        )
        if bot_is_admin:
            print("OK: bot is an administrator in the channel")
        else:
            print("WARN: bot is NOT an administrator in the channel — subscription check will fail")
    except Exception as exc:
        print(f"FAIL: {exc}")
        if "Cannot connect to host api.telegram.org" in str(exc):
            print("Hint: enable VPN or set BOT_PROXY in .env (e.g. socks5://127.0.0.1:1080)")
        sys.exit(1)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
