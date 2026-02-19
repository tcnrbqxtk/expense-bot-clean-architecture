from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka, inject

from application.interactors.user.change_currency import ChangeCurrencyInteractor
from application.interactors.user.change_daily_limit import ChangeDailyLimitInteractor
from application.interactors.user.get_user_settings import GetUserSettingsInfoInteractor
from presentation.states.settings_state import SettingsMenu


router = Router()


@router.message(Command("settings"), StateFilter(None))
@inject
async def settings_handler(
    message: Message,
    state: FSMContext,
    get_settings_info: FromDishka[GetUserSettingsInfoInteractor],
) -> None:
    settings_text = await get_settings_info(message.from_user.id if message.from_user else 0)
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
@inject
async def currency_choose(
    message: Message,
    state: FSMContext,
    change_currency: FromDishka[ChangeCurrencyInteractor],
    display_settings_info: FromDishka[GetUserSettingsInfoInteractor],
) -> None:
    if not message.from_user or message.text is None:
        return
    new_currency = message.text.strip().upper()
    await change_currency(message.from_user.id, new_currency)
    await message.answer(f"Валюта успешно изменена на {new_currency}!")
    settings_text = await display_settings_info(message.from_user.id if message.from_user else 0)
    await message.answer(settings_text, parse_mode="HTML")
    await state.set_state(SettingsMenu.choosing_action)


@router.message(SettingsMenu.waiting_for_limit)
@inject
async def limit_choose(
    message: Message,
    state: FSMContext,
    change_daily_limit: FromDishka[ChangeDailyLimitInteractor],
    display_settings_info: FromDishka[GetUserSettingsInfoInteractor],
) -> None:
    if not message.from_user or message.text is None:
        return
    try:
        new_limit = int(message.text.strip())
        await change_daily_limit(message.from_user.id, new_limit)
        await message.answer(f"Дневной лимит успешно изменён на {new_limit}!")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для дневного лимита.")
        await state.set_state(SettingsMenu.waiting_for_limit)
        return
    settings_text = await display_settings_info(message.from_user.id if message.from_user else 0)
    await message.answer(settings_text, parse_mode="HTML")
    await state.set_state(SettingsMenu.choosing_action)
