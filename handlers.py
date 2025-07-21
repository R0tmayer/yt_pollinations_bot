import os
import zipfile
import tempfile
import asyncio
import aiohttp
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import GenStates
from keyboards import main_menu_kb, back_kb, params_menu_kb, model_kb, yes_no_kb, skip_kb
from image_generation import generate_image

router = Router()

DEFAULT_PARAMS = {
    "model": "flux", "seed": None, "width": 1920, "height": 1080,
    "image": None, "enhance": False, "transparent": False, "nologo": "true"
}

PARAMS_LABELS = {
    "model": "Модель", "seed": "Seed", "width": "Ширина", "height": "Высота",
    "image": "Референс", "enhance": "Улучшить промты", "transparent": "Прозрачный фон"
}

async def show_params_menu(message, state):
    data = await state.get_data()
    params = data.get("params", DEFAULT_PARAMS.copy())
    params_text = (
        f"<b>🎨 Модель:</b> {params.get('model', 'flux')}\n"
        f"<b>🎲 Seed:</b> {params['seed'] if params['seed'] is not None else 'случайный'}\n"
        f"<b>↕️ Высота:</b> {params.get('height', 1080)} px\n"
        f"<b>↔️ Ширина:</b> {params.get('width', 1920)} px\n"
        f"<b>🖼️ Референс:</b> {params['image'] if params['image'] else 'нет'}\n"
        f"<b>🔮 Улучшить промты:</b> {'Да' if params.get('enhance') else 'Нет'}"
    )
    if params.get('model') == 'gptimage':
        params_text += f"\n<b>💨 Прозрачный фон:</b> {'Да' if params.get('transparent') else 'Нет'}"
    await message.answer(
        f"⚙️ <b>Параметры генерации:</b>\n\n{params_text}\n\n"
        f"Как будете готовы, просто прикрепите .txt файл с промтами",
        reply_markup=params_menu_kb(show_transparent=(params.get('model') == 'gptimage')),
        parse_mode='HTML'
    )
    await state.set_state(GenStates.menu)

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 <b>Добро пожаловать в мир нейро-арта!</b>\n\n"
        "Я — ваш персональный ИИ-художник. Просто дайте мне идею, и я превращу её в уникальное изображение.\n\n"
        "Готовы творить? Нажмите 'Создать шедевр'!",
        reply_markup=main_menu_kb(), parse_mode='HTML'
    )

@router.message(F.text == "✨ Создать шедевр")
@router.message(Command("generate"))
async def start_gen(message: types.Message, state: FSMContext):
    # Проверяем, есть ли параметры в состоянии, и если нет - инициализируем
    data = await state.get_data()
    if "params" not in data:
        await state.update_data(params=DEFAULT_PARAMS.copy())
    
    await show_params_menu(message, state)

@router.message(GenStates.menu, F.text)
async def params_menu_handler(message: types.Message, state: FSMContext):
    text = message.text
    if text.startswith("🎨"):
        await message.answer("Выберите модель из списка:", reply_markup=model_kb())
        await state.set_state(GenStates.edit_model)
    elif text.startswith("🎲"):
        await message.answer("Введите seed (любое целое число) или оставьте по умолчанию.", reply_markup=skip_kb())
        await state.set_state(GenStates.edit_seed)
    elif text.startswith("↔️"):
        await message.answer("Введите желаемую ширину изображения в пикселях.", reply_markup=skip_kb())
        await state.set_state(GenStates.edit_width)
    elif text.startswith("↕️"):
        await message.answer("Введите желаемую высоту изображения в пикселях.", reply_markup=skip_kb())
        await state.set_state(GenStates.edit_height)
    elif text.startswith("🖼️"):
        await message.answer("Отправьте прямую ссылку (URL) на изображение-референс или оставьте поле пустым.", reply_markup=skip_kb())
        await state.set_state(GenStates.edit_ref_image)
    elif text.startswith("🔮"):
        await message.answer("Хотите, чтобы нейросеть улучшила ваши промты для более детализированного результата?", reply_markup=yes_no_kb())
        await state.set_state(GenStates.edit_enhance)
    elif text.startswith("💨"):
        data = await state.get_data()
        if data.get("params", {}).get("model") != "gptimage":
            await message.answer("❗️ Эта опция доступна только для модели gptimage.")
            return
        await message.answer("Создать изображение с прозрачным фоном?", reply_markup=yes_no_kb())
        await state.set_state(GenStates.edit_transparent)
    elif text == "⬅️ В главное меню":
        await state.set_state(None) # Просто выходим из FSM
        # Отправляем новое сообщение с главной клавиатурой
        await message.answer(
            "👋 <b>Добро пожаловать в мир нейро-арта!</b>\n\n"
            "Я — ваш персональный ИИ-художник. Просто дайте мне идею, и я превращу её в уникальное изображение.\n\n"
            "Готовы творить? Нажмите 'Создать шедевр'!",
            reply_markup=main_menu_kb(), parse_mode='HTML'
        )

@router.message(GenStates.edit_model)
async def edit_model(message: types.Message, state: FSMContext):
    if message.text == "⬅️ В меню параметров":
        await show_params_menu(message, state)
        return
    
    # Исправляем парсинг, чтобы он брал последнее слово (название модели)
    model_name = message.text.split(' ')[-1]
    if model_name not in ["flux", "turbo", "kontext", "gptimage"]:
        await message.answer("Пожалуйста, выберите модель из списка.", reply_markup=model_kb())
        return
        
    data = await state.get_data()
    params = data.get("params", DEFAULT_PARAMS.copy())
    params["model"] = model_name
    if model_name != "gptimage":
        params["transparent"] = False
    await state.update_data(params=params)
    await show_params_menu(message, state)

# ... (Здесь будут остальные edit_* хендлеры, они аналогичны)
async def update_param_and_show_menu(message, state, param_name, value_processor=lambda x: x):
    if message.text == "⬅️ В меню параметров":
        await show_params_menu(message, state)
        return
    
    value = value_processor(message.text)
    if value is None and message.text != "⏭️ Оставить по умолчанию":
        # Просто оставим без изменений, если процессор не справился
        await show_params_menu(message, state)
        return

    data = await state.get_data()
    params = data.get("params", DEFAULT_PARAMS.copy())
    params[param_name] = value
    await state.update_data(params=params)
    await show_params_menu(message, state)

@router.message(GenStates.edit_seed)
async def edit_seed(message: types.Message, state: FSMContext):
    await update_param_and_show_menu(message, state, "seed", lambda x: int(x) if x.isdigit() else None)

@router.message(GenStates.edit_width)
async def edit_width(message: types.Message, state: FSMContext):
    await update_param_and_show_menu(message, state, "width", lambda x: int(x) if x.isdigit() else 1024)

@router.message(GenStates.edit_height)
async def edit_height(message: types.Message, state: FSMContext):
    await update_param_and_show_menu(message, state, "height", lambda x: int(x) if x.isdigit() else 1024)

@router.message(GenStates.edit_ref_image)
async def edit_ref_image(message: types.Message, state: FSMContext):
    await update_param_and_show_menu(message, state, "image", lambda x: x if x != "⏭️ Оставить по умолчанию" else None)

@router.message(GenStates.edit_enhance)
async def edit_enhance(message: types.Message, state: FSMContext):
    await update_param_and_show_menu(message, state, "enhance", lambda x: x == "✅ Да")

@router.message(GenStates.edit_transparent)
async def edit_transparent(message: types.Message, state: FSMContext):
    await update_param_and_show_menu(message, state, "transparent", lambda x: x == "✅ Да")

@router.message(GenStates.menu, F.document)
async def handle_file(message: types.Message, state: FSMContext, bot):
    doc = message.document
    if not doc.file_name.endswith(".txt"):
        await message.answer("❗️Пожалуйста, отправьте .txt файл с промтами.")
        return
    user_data = await state.get_data()
    params = user_data.get("params", DEFAULT_PARAMS.copy())
    status_msg = await message.answer("✅ Файл получен! Начинаю генерацию изображений... ⏳")
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, doc.file_name)
        await bot.download(doc, destination=file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            prompts = [line.strip() for line in f if line.strip()]
        if not prompts:
            await status_msg.edit_text("❗️Файл пустой или некорректный.")
            return
        images_dir = os.path.join(tmpdir, "images")
        os.makedirs(images_dir, exist_ok=True)
        image_paths = []
        total = len(prompts)
        async with aiohttp.ClientSession() as session:
            for idx, prompt in enumerate(prompts, 1):
                img = await generate_image(session, prompt, params)
                if img:
                    img_path = os.path.join(images_dir, f"image_{idx}.jpg")
                    with open(img_path, "wb") as out:
                        out.write(img)
                    image_paths.append(img_path)
                await status_msg.edit_text(f"🖼️ Генерирую изображения: {idx} из {total}... ⏳")
                await asyncio.sleep(0.5)
        if not image_paths:
            await status_msg.edit_text("❗️Не удалось сгенерировать ни одной картинки.")
            return
        await status_msg.edit_text("📦 Генерация завершена! Формирую архив...")
        zip_path = os.path.join(tmpdir, "images.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for img_path in image_paths:
                zipf.write(img_path, os.path.basename(img_path))
        await status_msg.edit_text("📤 Отправляю архив с картинками...")
        with open(zip_path, "rb") as zipf:
            await message.answer_document(
                types.FSInputFile(zipf.name, filename="images.zip"),
                caption="✅ Ваш архив с картинками готов! Спасибо за использование бота.\n\n🏠 Для возврата в меню используйте кнопку ниже.",
                reply_markup=main_menu_kb()
            )
        await status_msg.delete()
    await state.clear() 