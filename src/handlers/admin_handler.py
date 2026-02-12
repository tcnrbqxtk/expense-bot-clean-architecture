from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.admin_state import AdminMenu
from storage.json_storage import check_admin, clear_user, get_active_users, get_all_messages_count


router = Router()

choice_text = (
    "Выберите действие:\n"
    "1️⃣ Посмотреть количество пользователей\n"
    "2️⃣ Сбросить данные пользователя\n"
    "<pre>/return — вернуться в меню при вводе ID пользователя</pre>\n"
    "3️⃣ Агрегированная статистика\n"
    "<pre>"
    "/quit — выход из админ-панели"
    "</pre>"
)


@router.message(Command("admin"))
async def admin_start(message: Message, state: FSMContext) -> None:
    if not message.from_user or not check_admin(message.from_user.id):
        return
    await message.answer(choice_text, parse_mode="HTML")
    await state.set_state(AdminMenu.choosing_action)


# Выбор действия
@router.message(AdminMenu.choosing_action)
async def admin_choose(message: Message, state: FSMContext) -> None:
    if not message.from_user:
        return
    text = (message.text or "").strip()
    if text == "/quit":
        await message.answer("Выход из админ-панели.")
        await state.clear()
    elif text == "1" or "количество" in text.lower():
        await message.answer(f"Всего пользователей: {get_active_users()}")
        await state.set_state(AdminMenu.choosing_action)
    elif text == "2" or "сброс" in text.lower():
        await state.set_state(AdminMenu.waiting_for_user_id)
        await message.answer("Введите ID пользователя, чьи данные нужно сбросить:")
    elif text == "3" or "статистика" in text.lower():
        await message.answer(
            f"Агрегированная статистика:\n"
            f"Всего пользователей: {get_active_users()}\n"
            f"Общее количество расходов: {get_all_messages_count()}"
        )
        await state.set_state(AdminMenu.choosing_action)

    else:
        await message.answer("Неверный выбор, попробуйте снова.")


@router.message(AdminMenu.waiting_for_user_id)
async def admin_reset_user(message: Message, state: FSMContext) -> None:
    if not message.from_user or message.text is None:
        return
    try:
        user_id = int(message.text or "")
        clear_user(user_id)
        await message.answer(f"Данные пользователя {user_id} сброшены.")
    except ValueError:
        if message.text == "/return":
            await message.answer(choice_text)
        else:
            await message.answer("ID должно быть числом, попробуйте снова.")
            return
    await state.set_state(AdminMenu.choosing_action)
