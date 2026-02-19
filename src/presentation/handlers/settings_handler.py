from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.settings_state import SettingsMenu
from storage.json_storage import change_settings, get_settings_info


router = Router()


def display_settings_info(user_id: int) -> str:
    settings_info = get_settings_info(user_id)
    return (
        "<b>⚙️ Настройки бота:</b>\n\n"
        "Здесь вы можете изменить настройки бота.\n\n"
        "<i>Доступные настройки:</i>\n"
        "<pre>"
        "1) Валюта (текущая: " + (settings_info["currency"] if settings_info else "RUB") + ")\n"
        "2) Дневной Лимит (текущий: " + (str(settings_info["daily_limit"]) if settings_info else "0") + ")\n"
        "</pre>"
        "/quit - Выйти из меню настроек"
    )


@router.message(Command("settings"), StateFilter(None))
async def settings_handler(message: Message, state: FSMContext) -> None:
    settings_text = display_settings_info(message.from_user.id if message.from_user else 0)
    await message.answer(settings_text, parse_mode="HTML")
    await state.set_state(SettingsMenu.choosing_action)


@router.message(SettingsMenu.choosing_action)
async def settings_choose(message: Message, state: FSMContext) -> None:
    if not message.from_user:
        return
    text = (message.text or "").strip().lower()
    if text == "/quit":
        await state.clear()
    elif text == "валюта" or "1" in text:
        await message.answer("Введите новую валюту (например, USD, EUR, RUB):")
        await state.set_state(SettingsMenu.waiting_for_currency)
    elif text == "дневной лимит" or "2" in text:
        await message.answer("Введите новый дневной лимит (число):")
        await state.set_state(SettingsMenu.waiting_for_limit)
    else:
        await message.answer("Неверный выбор, попробуйте снова.")


@router.message(SettingsMenu.waiting_for_currency)
async def currency_choose(message: Message, state: FSMContext) -> None:
    if not message.from_user or message.text is None:
        return
    new_currency = message.text.strip().upper()
    change_settings(message.from_user.id, new_currency)
    await message.answer(f"Валюта успешно изменена на {new_currency}!")
    settings_text = display_settings_info(message.from_user.id if message.from_user else 0)
    await message.answer(settings_text, parse_mode="HTML")
    await state.set_state(SettingsMenu.choosing_action)


@router.message(SettingsMenu.waiting_for_limit)
async def limit_choose(message: Message, state: FSMContext) -> None:
    if not message.from_user or message.text is None:
        return
    try:
        new_limit = int(message.text.strip())
        change_settings(message.from_user.id, daily_limit=new_limit)
        await message.answer(f"Дневной лимит успешно изменён на {new_limit}!")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для дневного лимита.")
        await state.set_state(SettingsMenu.waiting_for_limit)
        return
    settings_text = display_settings_info(message.from_user.id if message.from_user else 0)
    await message.answer(settings_text, parse_mode="HTML")
    await state.set_state(SettingsMenu.choosing_action)
