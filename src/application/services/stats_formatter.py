from typing import List
from domain.entities.expense import Expense


class StatsFormatterService:
    """Service for formatting statistics about expenses."""

    def __call__(self, expenses: List[Expense], period_name: str, currency: str) -> str:
        if not expenses:
            return "Расходов за указанный период не найдено."

        summary: dict[str, float] = {}
        comments: dict[str, list[str]] = {}

        for e in expenses:
            summary[e.category] = summary.get(e.category, 0) + e.amount
            if e.comment:
                comments.setdefault(e.category, []).append(e.comment)

        result = f"Статистика за {period_name}:\n"

        for category, total in summary.items():
            result += f"{category.title()} - {total} {currency}"

            if comments.get(category):
                unique = {c: comments[category].count(c) for c in set(comments[category])}
                parts = [f"{c} - {cnt}" if cnt > 1 else c for c, cnt in unique.items()]
                result += " (" + ", ".join(parts) + ")"

            result += "\n"

        return result
