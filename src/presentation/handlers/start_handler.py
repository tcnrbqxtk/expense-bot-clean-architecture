from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message


router = Router()


@router.message(CommandStart(), StateFilter(None))
async def start_handler(message: Message) -> None:
    start_text = (
        "<b>👋  Привет! Я простой бот для хранения твоих трат!</b>\n\n"
        "Вот мой интерфейс:\n\n"
        "<b>/add <i>сумма категория комментарий</i></b> — добавить расход (комментарий не обязателен)\n"
        "<b>/clear</b> — удалить все расходы\n"
        "<b>/settings</b> — настройки бота\n\n"
        "<b>/stats</b> — статистика расходов:\n"
        "<pre>"
        "/stats       — за всё время\n"
        "/stats   *   — за последние * дней\n"
        "/stats today — за сегодня\n"
        "/stats week  — за текущую неделю\n"
        "/stats month — за текущий месяц\n"
        "/stats year  — за текущий год"
        "</pre>\n\n"
    )
    await message.answer(start_text, parse_mode="HTML")
