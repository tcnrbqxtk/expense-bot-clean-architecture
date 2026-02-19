from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.filters.command import CommandObject
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka, inject

from application.interactors.user.get_user import GetUserInteractor
from application.interactors.user.add_expense import AddExpenseInteractor
from application.interactors.user.create_user import CreateUserInteractor

from exceptions import ExpensesCapError, JsonError

router = Router()


@router.message(Command("add"), StateFilter(None))
@inject
async def add_handler(
    message: Message,
    command: CommandObject,
    add_expense: FromDishka[AddExpenseInteractor],
    create_user: FromDishka[CreateUserInteractor],
    get_user: FromDishka[GetUserInteractor]
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
        try:
            user = await create_user(message.from_user.id)
        except ValueError:
            user = await get_user(message.from_user.id)
        await add_expense(user, amount, category, comment) # type: ignore
    except ExpensesCapError:
        await message.answer("Превышено максимальное количество трат в день!")
        return
    except JsonError:
        await message.answer("Ошибка в базе данных. Данные не переданы")
        return

    await message.answer(f"💸 Расход {amount} ₽ добавлен в категорию «{category}»")
