from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.filters.command import CommandObject
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka, inject

from application.interactors.user.add_expense_for_user import GetOrCreateUserAndAddExpenseInteractor
from exceptions import ExpensesCapError, JsonError


router = Router()


@router.message(Command("add"), StateFilter(None))
@inject
async def add_handler(
    message: Message, command: CommandObject, get_or_create_and_add: FromDishka[GetOrCreateUserAndAddExpenseInteractor]
) -> None:

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
    comment = parts[2] if len(parts) > 2 else ""

    try:
        await get_or_create_and_add(message.from_user.id, amount, category, comment)
    except ExpensesCapError:
        await message.answer("Ошибка: Превышен лимит расходов!")
        return
    except JsonError:
        await message.answer("Ошибка при сохранении расхода.")
        return
    except PermissionError:
        await message.answer(
            "Ошибка: У вас нет прав для добавления расходов. (скорее всего ошибка со стороны базы данных)"
        )
        return
    await message.answer(f"💸 Расход {amount} ₽ добавлен в категорию «{category}»")
