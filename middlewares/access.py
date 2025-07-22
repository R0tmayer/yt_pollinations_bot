from aiogram import BaseMiddleware
from aiogram.types import Message
from services.user_service import is_user_allowed

class AccessMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        allowed = await is_user_allowed(event.from_user.username)
        if not allowed:
            await event.answer(
                "У вас нет доступа.\n\n Для получения доступа напишите @R0tmayer или @pirat_youtubov"
            )
            state = data.get("state")
            if state:
                await state.clear()
            return
        return await handler(event, data) 