from domain.entities.expense import Expense
from domain.entities.role import Role
from domain.entities.user import User
from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository
from exceptions import JsonError


class GetOrCreateUserAndAddExpenseInteractor:
    def __init__(self, user_repo: UserRepository, expense_repo: ExpenseRepository, admin_ids: list[str]):
        self.user_repo = user_repo
        self.expense_repo = expense_repo
        self.admin_ids = admin_ids

    async def __call__(self, user_id: int, amount: float, category: str, comment: str) -> None:
        # Get or create the user
        user = self.user_repo.get(user_id)
        if not user:
            role = Role("admin") if str(user_id) in self.admin_ids else Role("user")
            user = User(user_id, role)
            self.user_repo.add(user)

        # Create an expense for the user
        if not user.role.can_add():
            raise PermissionError("User does not have permission to add expenses")
        expense = Expense(user.user_id, amount, category, comment)
        try:
            self.expense_repo.add(expense)
        except JsonError as e:
            raise JsonError(f"Failed to add expense: {e}")

        return
