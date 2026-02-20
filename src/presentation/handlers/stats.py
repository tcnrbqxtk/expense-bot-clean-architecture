import logging

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.filters.command import CommandObject
from dishka.integrations.aiogram import FromDishka, inject

from application.interactors.user.get_stats_by_period import GetStatsByPeriodInteractor


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("stats"), StateFilter(None))
@inject
async def get_stats(
    message: types.Message,
    command: CommandObject,
    get_stats_by_period_interactor: FromDishka[GetStatsByPeriodInteractor],
) -> None:
    if not message.from_user:
        return
    if not command.args:
        result = await get_stats_by_period_interactor(message.from_user.id, "0")
        await message.answer(result, parse_mode="HTML")
        return
    parts = command.args.split(maxsplit=1)
    period = 0
    try:
        period = parts[0]
    except ValueError:
        period = parts[0].lower()
    result = await get_stats_by_period_interactor(message.from_user.id, period)
    await message.answer(result, parse_mode="HTML")
