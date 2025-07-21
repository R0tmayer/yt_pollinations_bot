import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage # Импортируем хранилище
from dotenv import load_dotenv
from handlers import router
import image_generation

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("POLLINATIONS_API_KEY")

image_generation.API_KEY = API_KEY

# Создаем хранилище для состояний FSM
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage) # Передаем хранилище в диспетчер
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())