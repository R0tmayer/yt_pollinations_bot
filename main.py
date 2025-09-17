import os
import json
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers.user_handlers import user_router
from handlers.generation_handlers import generation_router
from services import image_service

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Expect JSON array of tokens in POLLINATIONS_API_TOKENS.
raw_tokens = os.getenv("POLLINATIONS_API_TOKENS", "[]")
parsed = json.loads(raw_tokens)
tokens = [str(t).strip() for t in parsed]

image_service.API_TOKENS = tokens

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)
dp.include_router(user_router)
dp.include_router(generation_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
