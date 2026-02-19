from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from storage.json_storage import delete_user_expenses


router = Router()


@router.message(Command("clear"), StateFilter(None))
async def get_stats(message: types.Message) -> None:
    if not message.from_user:
        return
    delete_user_expenses(message.from_user.id)
    await message.answer("Расходы успешно очищены!\n")
