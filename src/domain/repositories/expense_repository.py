from typing import Protocol

from domain.entities.expense import Expense


class ExpenseRepository(Protocol):
    def add(self, expense: Expense) -> None:
        """Add expense"""
        ...

    def get_by_user(self, user_id: int) -> list[Expense]:
        """Get all expenses for a user"""
        ...

    def clear(self, user_id: int) -> None:
        """Clear all expenses for a user"""
        ...

    def count_all_expenses(self) -> float:
        """Returns sum of all expenses in the repository"""
        ...

    def get_all(self) -> list[Expense]:
        """Returns all expenses in the repository"""
        ...
