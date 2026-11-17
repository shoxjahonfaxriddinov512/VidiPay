import os
import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ["BOT_TOKEN"]
BUTTON_URL = os.environ.get("BUTTON_URL", "https://example.com")
BUTTON_TEXT = os.environ.get("BUTTON_TEXT", "🚀 Boshlash")
PORT = int(os.environ.get("PORT", 10000))

WELCOME_TEXT = (
    "👋 <b>Xush kelibsiz!</b>\n\n"
    "🎬 Bu yerga o'zingizning matningizni yozing.\n"
    "👥 Istagan matn, emoji va <b>qalin</b> yozuvlardan foydalanishingiz mumkin.\n\n"
    "Boshlash uchun pastdagi tugmani bosing 👇"
)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=BUTTON_TEXT, url=BUTTON_URL)]]
    )
    await message.answer(WELCOME_TEXT, reply_markup=kb)


# UptimeRobot shu manzilni ping qiladi
async def health(request):
    return web.Response(text="OK")


async def main():
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
