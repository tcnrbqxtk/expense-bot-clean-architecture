from domain.entities import user
from domain.entities.expense import Expense
from domain.repositories.expense_repository import ExpenseRepository
from exceptions import JsonError


class AddExpenseInteractor:
    def __init__(self, expense_repo: ExpenseRepository) -> None:
        self.expense_repo = expense_repo

    async def __call__(self, user: user.User, amount: float, category: str, comment: str = "") -> None:
        if not user.role.can_add():
            raise PermissionError("User does not have permission to add expenses")
        expense = Expense(user.user_id, amount, category, comment)
        try:
            await self.expense_repo.add(expense)
        except JsonError as e:
            raise JsonError(f"Failed to add expense: {e}")
