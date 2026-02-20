from typing import Any

from domain.entities.expense import Expense
from domain.repositories.expense_repository import ExpenseRepository
from exceptions import JsonError

from datetime import date


class JsonExpenseRepository(ExpenseRepository):
    def __init__(self, path: str):
        self.path = path

    def _load_expenses(self) -> dict[str, Any]:
        import json

        try:
            with open(self.path) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            raise JsonError("Invalid JSON format in expenses file")

    def _save_expenses(self, data: dict[str, list[dict[str, str | float]]]) -> None:
        import json

        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    async def add(self, expense: Expense) -> None:
        data = self._load_expenses()
        user_expenses = data.get(str(expense.user_id), [])
        user_expenses.append(
            {
                "amount": expense.amount,
                "category": expense.category,
                "comment": expense.comment,
                "date": expense.date.isoformat(),
            }
        )
        data[str(expense.user_id)] = user_expenses
        self._save_expenses(data)

    async def get_by_user(self, user_id: int) -> list[Expense]:
        data = self._load_expenses()
        user_expenses = data.get(str(user_id), [])
        return [
            Expense(user_id, e["amount"], e["category"], e["comment"], date.fromisoformat(e["date"]))
            for e in user_expenses
        ]

    async def clear(self, user_id: int) -> None:
        data = self._load_expenses()
        if str(user_id) in data:
            del data[str(user_id)]
            self._save_expenses(data)

    async def count_all_expenses(self) -> float:
        data = self._load_expenses()
        return sum(e["amount"] for expenses in data.values() for e in expenses)

    async def get_all(self) -> list[Expense]:
        data = self._load_expenses()
        expenses: list[Expense] = []
        for user_id, user_expenses in data.items():
            expenses.extend(
                Expense(int(user_id), e["amount"], e["category"], e["comment"], e["date"]) for e in user_expenses
            )
        return expenses
