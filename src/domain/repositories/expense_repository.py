from typing import Protocol

from domain.entities.expense import Expense


class ExpenseRepository(Protocol):
    def add_expense(self, expense: Expense) -> None:
        """Add expense"""
        ...

    def get_expenses_by_user(self, user_id: int) -> list[Expense]:
        """Get all expenses for a user"""
        ...

    def clear_expenses(self, user_id: int) -> None:
        """Clear all expenses for a user"""
        ...

    def count_all_expenses(self) -> float:
        """Returns sum of all expenses in the repository"""
        ...

    def get_all_expenses(self) -> list[Expense]:
        """Returns all expenses in the repository"""
        ...
