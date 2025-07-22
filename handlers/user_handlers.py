from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards import main_menu_kb
from services.user_service import is_user_allowed      

user_router = Router()

@user_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    allowed = await is_user_allowed(message.from_user.username)
    if not allowed:
        await message.answer("У вас нет доступа.\n\n Для получения доступа напишите @R0tmayer или @pirat_youtubov")
        await state.clear()
        return
    await state.clear()
    await message.answer(
        "👋 <b>Добро пожаловать в мир нейро-арта!</b>\n\n"
        "Я — ваш персональный ИИ-художник. Просто дайте мне идею, и я превращу её в уникальное изображение.\n\n"
        "Готовы творить? Нажмите 'Создать шедевр'!",
        reply_markup=main_menu_kb(), parse_mode='HTML'
    )

@user_router.message(F.text == "⬅️ В главное меню")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await message.answer(
        "👋 <b>Добро пожаловать в мир нейро-арта!</b>\n\n"
        "Я — ваш персональный ИИ-художник. Просто дайте мне идею, и я превращу её в уникальное изображение.\n\n"
        "Готовы творить? Нажмите 'Создать шедевр'!",
        reply_markup=main_menu_kb(), parse_mode='HTML'
    ) 