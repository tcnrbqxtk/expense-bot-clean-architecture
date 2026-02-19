from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from states.admin_state import AdminMenu


router = Router()


@router.message(Command("help"), StateFilter(None))
async def help_handler(message: Message) -> None:
    help_text = (
        "<b>Помощь по командам:</b>\n\n"
        "<b>/start</b> — начать работу с ботом\n"
        "<b>/add <i>сумма категория комментарий</i></b> — добавить расход (комментарий не обязателен)\n"
        "<b>/clear</b> — удалить все расходы\n\n"
        "<b>/stats</b> — статистика расходов:\n"
        "<pre>"
        "/stats       — за всё время\n"
        "/stats   *   — за последние * дней\n"
        "/stats today — за сегодня\n"
        "/stats week  — за текущую неделю\n"
        "/stats month — за текущий месяц\n"
        "/stats year  — за текущий год"
        "</pre>"
    )
    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("help"), StateFilter(AdminMenu.choosing_action))
async def admin_help_handler(message: Message) -> None:
    admin_help_text = (
        "<b>🛠 Помощь по админ-панели:</b>\n\n"
        "<b>/admin</b> — вход в админ-панель\n"
        "<b>/help</b> — показать эту справку\n"
        "<b>/quit</b> — выход из админ-панели\n\n"
        "<b>Действия в меню:</b>\n"
        "<pre>"
        "1/количество — количество пользователей\n"
        "2/сброс      — сброс данных пользователя\n"
        "3/статистика — агрегированная статистика\n"
        "</pre>\n"
        "<b>Дополнительно:</b>\n"
        "<pre>"
        "/return — вернуться в меню при вводе ID пользователя\n"
        "</pre>"
    )

    await message.answer(admin_help_text, parse_mode="HTML")
