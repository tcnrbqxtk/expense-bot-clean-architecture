import logging

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.filters.command import CommandObject
from storage.json_storage import user_get_by_period


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("stats"), StateFilter(None))
async def get_stats(message: types.Message, command: CommandObject) -> None:
    if not message.from_user:
        return
    if not command.args:
        await message.answer(str(user_get_by_period(message.from_user.id, 0)))
        return
    parts = command.args.split(maxsplit=1)
    period = 0
    try:
        period = int(parts[0])
    except ValueError:
        period = parts[0].lower()
    await message.answer(str(user_get_by_period(message.from_user.id, period)), parse_mode="HTML")
