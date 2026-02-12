from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import json
import logging
from typing import Any
import uuid


import config
from exceptions import ExpensesCapError, JsonError


logger = logging.getLogger(__name__)


def load_data() -> dict[str, dict[Any, Any]]:
    try:
        with open(config.DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {"users": {}}


def save_data(data: dict[str, dict[Any, Any]]) -> None:
    with open(config.DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_expense(
    user_id: int, amount: int, category: str = "", comment: str = "", curr: str = "RUB", daily_limit: int = 0
) -> None:
    data: dict[str, dict[Any, Any]] = load_data()
    uid = str(user_id)
    role = "user"
    if uid in config.ADMIN_IDS:
        role = "admin"

    if uid in data["users"]:
        try:
            if len(data["users"][uid]["expenses"]) > 30:
                raise ExpensesCapError
        except KeyError as e:
            logger.warning(e)
            raise JsonError from None

    data["users"].setdefault(
        uid, ({"role": role, "settings": {"currency": curr, "daily_limit": daily_limit}, "expenses": []})
    )

    data["users"][uid]["expenses"].append(
        {
            "id": str(uuid.uuid4()),
            "amount": amount,
            "category": category.lower(),
            "comment": comment.lower(),
            "date": date.today().isoformat(),
        }
    )

    save_data(data)


def get_week_bounds(today: date | None = None) -> tuple[date, date]:
    today = today or date.today()
    start_of_week = today - timedelta(days=today.weekday())  # понедельник
    end_of_week = start_of_week + timedelta(days=6)  # воскресенье
    return start_of_week, end_of_week


def get_month_bounds(today: date | None = None) -> tuple[date, date]:
    today = today or date.today()
    start_of_month = today.replace(day=1)
    end_of_month = start_of_month + relativedelta(months=1) - timedelta(days=1)
    return start_of_month, end_of_month


def get_year_bounds(today: date | None = None) -> tuple[date, date]:
    today = today or date.today()
    start_of_year = date(today.year, 1, 1)
    end_of_year = date(today.year, 12, 31)
    return start_of_year, end_of_year


def get_period_info(period: str | int = "0") -> dict[str, Any]:
    wrong_input_marker = False

    today = date.today()
    date_floor = date(1970, 1, 1)
    date_ceil = today
    result_period = "всё время"

    # 🔢 ЧИСЛА — последние N дней (оставляем как есть)
    if isinstance(period, int):
        if period < 0 or period > 1_000_000:
            wrong_input_marker = True
        elif period == 0:
            result_period = "всё время"
        else:
            date_floor = today - timedelta(days=period - 1)
            date_ceil = today
            result_period = f"период {period} дней" if period > 1 else "последний день"

    # 📅 СЕГОДНЯ
    elif period == "today":
        date_floor = today
        date_ceil = today
        result_period = "сегодня"

    # 🗓️ ТЕКУЩАЯ НЕДЕЛЯ (календарная)
    elif period == "week":
        date_floor, date_ceil = get_week_bounds(today)
        result_period = "текущую неделю"

    # 🗓️ ТЕКУЩИЙ МЕСЯЦ
    elif period == "month":
        date_floor, date_ceil = get_month_bounds(today)
        result_period = "текущий месяц"

    # 🗓️ ТЕКУЩИЙ ГОД
    elif period == "year":
        date_floor, date_ceil = get_year_bounds(today)
        result_period = "текущий год"

    else:
        wrong_input_marker = True

    result = "\n" if wrong_input_marker else f"Статистика за {result_period}:\n"

    return {
        "date_floor": date_floor,
        "date_ceil": date_ceil,
        "wrong_input_marker": wrong_input_marker,
        "result": result,
    }


def user_get_by_period(user_id: int, period: str | int = "0") -> str:
    data = load_data()
    uid = str(user_id)

    if uid not in data.get("users", {}):
        return "Ошибка: пользователь не найден. Пожалуйста, добавьте расход с помощью команды /add, чтобы начать использовать бота."

    period_info = get_period_info(period)
    if period_info["wrong_input_marker"]:
        return (
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

    expenses_list = data["users"][uid].get("expenses", [])
    if not expenses_list:
        return "Расходов за указанный период не найдено."

    processed_expenses: dict[str, int] = {}
    processed_comments: dict[str, list[str]] = {}

    for expense in expenses_list:
        try:
            expense_date = date.fromisoformat(expense["date"])
            if period_info["date_floor"] <= expense_date <= period_info["date_ceil"]:
                category = expense["category"]
                amount = expense["amount"]
                comment = expense.get("comment", "")

                processed_expenses[category] = processed_expenses.get(category, 0) + amount
                if comment:
                    processed_comments.setdefault(category, []).append(comment)

        except (KeyError, TypeError, ValueError) as e:
            logger.warning(f"Ошибка в записи расхода: {e}")
            continue

    if not processed_expenses:
        return "Расходов за указанный период не найдено."

    result_text = f"{period_info['result']}" if period_info["result"].strip() else ""

    for category, total in processed_expenses.items():
        result_text += f"{category.title()} - {total} {data['users'][uid]['settings']['currency']}"

        comments = processed_comments.get(category, [])
        if comments:
            comment_count: dict[str, int] = {}
            for c in comments:
                comment_count[c] = comment_count.get(c, 0) + 1

            comment_parts = [f"{c} - {count}" if count > 1 else f"{c}" for c, count in comment_count.items()]
            result_text += " (" + ", ".join(comment_parts) + ")"

        result_text += "\n"

    return result_text


def delete_user_expenses(user_id: int) -> None:
    data = load_data()
    uid = str(user_id)

    if uid in data["users"]:
        data["users"][uid]["expenses"] = []
        save_data(data)


def check_admin(user_id: int) -> bool:
    data = load_data()
    uid = str(user_id)
    return uid in data["users"] and data["users"][uid].get("role") == "admin"


def get_active_users() -> int:
    data = load_data()
    return len(data["users"])


def get_all_messages_count() -> int:
    data = load_data()
    count = 0
    for user in data["users"].values():
        count += len(user.get("expenses", []))
    return count


def clear_user(user_id: int) -> None:
    data: dict[str, dict[Any, Any]] = load_data()
    uid = str(user_id)

    data["users"].setdefault(uid, ({"role": "user", "settings": {"currency": "RUB", "daily_limit": 0, "expenses": []}}))

    save_data(data)


def change_settings(user_id: int, curr: str | None = None, daily_limit: int | None = None) -> None:
    data: dict[str, dict[Any, Any]] = load_data()
    uid = str(user_id)
    role = "user"
    if uid in config.ADMIN_IDS:
        role = "admin"

    data["users"].setdefault(uid, ({"role": role, "settings": {"currency": "RUB", "daily_limit": 0}, "expenses": []}))

    data["users"][uid]["settings"].update(
        {
            "currency": curr if curr is not None else data["users"][uid]["settings"]["currency"],
            "daily_limit": daily_limit if daily_limit is not None else data["users"][uid]["settings"]["daily_limit"],
        }
    )

    save_data(data)


def check_daily_limit(user_id: int) -> bool:
    data = load_data()
    uid = str(user_id)

    if uid not in data["users"]:
        return False

    daily_limit = data["users"][uid]["settings"].get("daily_limit", 0)
    if daily_limit <= 0:
        return False

    today = date.today()
    total_today = sum(
        expense["amount"]
        for expense in data["users"][uid].get("expenses", [])
        if expense.get("date") == today.isoformat()
    )

    return total_today > daily_limit


def get_settings_info(user_id: int) -> dict[str, Any] | None:
    data = load_data()
    uid = str(user_id)

    if uid not in data["users"]:
        return None

    settings = data["users"][uid].get("settings", {})
    return {
        "currency": settings.get("currency", "RUB"),
        "daily_limit": settings.get("daily_limit", 0),
    }
