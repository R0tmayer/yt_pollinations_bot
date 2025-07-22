from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu_kb(is_admin=False):
    kb = ReplyKeyboardBuilder()
    kb.button(text="✨ Создать шедевр")
    if is_admin:
        kb.button(text="👤 Выдать доступ")
    return kb.as_markup(resize_keyboard=True, is_persistent=True)

def back_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Назад")]],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Выберите действие..."
    )

def params_menu_kb(show_transparent: bool = False):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🎨 Модель"),
        KeyboardButton(text="🎲 Seed")
    )
    builder.row(
        KeyboardButton(text="↔️ Ширина"),
        KeyboardButton(text="↕️ Высота")
    )
    builder.row(
        KeyboardButton(text="🖼️ Референс"),
        KeyboardButton(text="🔮 Улучшить промты")
    )
    row_buttons = []
    if show_transparent:
        row_buttons.append(KeyboardButton(text="💨 Прозрачный фон"))
    builder.row(*row_buttons)
    builder.row(KeyboardButton(text="⬅️ В главное меню"))
    return builder.as_markup(resize_keyboard=True, is_persistent=True)

def model_kb():
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text="🎨 flux"), KeyboardButton(text="🚀 turbo"))
    kb.row(KeyboardButton(text="🖼️ kontext"), KeyboardButton(text="🤖 gptimage"))
    kb.row(KeyboardButton(text="⬅️ В меню параметров"))
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False, is_persistent=True)


def yes_no_kb():
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text="✅ Да"), KeyboardButton(text="❌ Нет"))
    kb.row(KeyboardButton(text="⬅️ В меню параметров"))
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False, is_persistent=True)


def skip_kb():
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text="⏭️ Оставить по умолчанию"))
    kb.row(KeyboardButton(text="⬅️ В меню параметров"))
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False, is_persistent=True)