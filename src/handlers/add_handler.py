from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.filters.command import CommandObject
from aiogram.types import Message

from exceptions import ExpensesCapError, JsonError
from storage.json_storage import add_expense, check_daily_limit


router = Router()


@router.message(Command("add"), StateFilter(None))
async def add_handler(message: Message, command: CommandObject) -> None:
    if not message.from_user:
        return

    if not command.args:
        await message.answer("Использование: /add сумма категория комментарий")
        return

    parts = command.args.split(maxsplit=2)

    if len(parts) < 2:
        await message.answer("Использование: /add сумма категория комментарий")
        return

    try:
        amount = int(parts[0])
        if amount <= 0:
            await message.answer("Ошибка: Сумма должна быть положительным числом!")
            return
    except ValueError:
        await message.answer("Ошибка: Сумма должна быть целым числом!")
        return

    category = parts[1]
    try:
        comment = parts[2]
    except (IndexError, ValueError):
        comment = ""
    try:
        add_expense(message.from_user.id, amount, category, comment)
    except ExpensesCapError:
        await message.answer("Превышено максимальное количество трат!")
        return
    except JsonError:
        await message.answer("Ошибка в базе данных. Данные не переданы")
        return

    await message.answer(f"💸 Расход {amount} ₽ добавлен в категорию «{category}»")
    if check_daily_limit(message.from_user.id):
        await message.answer("⚠️ Внимание! Вы превысили свой дневной лимит расходов!")
