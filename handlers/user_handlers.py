from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards import main_menu_kb
from services.user_service import is_user_allowed
from supabase import create_client
import os

user_router = Router()

ADMIN_USERNAMES = {"R0tmayer", "pirat_youtubov"}

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@user_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    is_admin = message.from_user.username in ADMIN_USERNAMES
    await state.clear()
    await message.answer(
        "👋 <b>Добро пожаловать в мир нейро-арта!</b>\n\n"
        "Я — ваш персональный ИИ-художник. Просто дайте мне идею, и я превращу её в уникальное изображение.\n\n"
        "Готовы творить? Нажмите 'Создать шедевр'!",
        reply_markup=main_menu_kb(is_admin=is_admin), parse_mode='HTML'
    )

@user_router.message(F.text == "⬅️ В главное меню")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    is_admin = message.from_user.username in ADMIN_USERNAMES
    await state.set_state(None)
    await message.answer(
        "👋 <b>Добро пожаловать в мир нейро-арта!</b>\n\n"
        "Я — ваш персональный ИИ-художник. Просто дайте мне идею, и я превращу её в уникальное изображение.\n\n"
        "Готовы творить? Нажмите 'Создать шедевр'!",
        reply_markup=main_menu_kb(is_admin=is_admin), parse_mode='HTML'
    )

@user_router.message(F.text == "👤 Выдать доступ")
async def ask_username(message: types.Message, state: FSMContext):
    await message.answer("Введите username пользователя (без @):")
    await state.set_state("wait_username_to_add")

@user_router.message(F.state == "wait_username_to_add")
async def add_user_to_db(message: types.Message, state: FSMContext):
    username = message.text.strip().lstrip("@")
    supabase.table("users").insert({"username": username}).execute()
    await message.answer(f"Пользователь @{username} добавлен в базу.")
    await state.clear() 