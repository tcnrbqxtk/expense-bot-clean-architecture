from domain.entities import user
from domain.entities.expense import Expense
from domain.repositories.expense_repository import ExpenseRepository


class AddExpenseInteractor:
    def __init__(self, expense_repo: ExpenseRepository):
        self.expense_repo = expense_repo

    async def __call__(self, user: user.User, amount: float, category: str, comment: str = ""):
        if not user.role.can_add_expense():
            raise PermissionError("User does not have permission to add expenses")
        expense = Expense(user.user_id, amount, category, comment)
        self.expense_repo.add_expense(expense)
