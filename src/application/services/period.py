from datetime import date, timedelta

from dateutil.relativedelta import relativedelta


class PeriodService:
    """Service for calculating date ranges based on a given period identifier."""

    def __call__(self, period: str | int = "0") -> tuple[date, date, str]:
        today = date.today()

        try:
            period = int(period)
            if period <= 0:
                return date(1970, 1, 1), today, "всё время"
            start = today - timedelta(days=period - 1)
            return start, today, f"период {period} дней"
        except TypeError:
            if period == "today":
                return today, today, "сегодня"

            if period == "week":
                start = today - timedelta(days=today.weekday())
                return start, start + timedelta(days=6), "текущую неделю"

            if period == "month":
                start = today.replace(day=1)
                end = start + relativedelta(months=1) - timedelta(days=1)
                return start, end, "текущий месяц"

            if period == "year":
                return date(today.year, 1, 1), date(today.year, 12, 31), "текущий год"

            return date(1970, 1, 1), today, "всё время"
