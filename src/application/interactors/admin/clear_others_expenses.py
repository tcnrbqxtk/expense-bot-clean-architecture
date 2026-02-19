from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository


class ClearOthersExpensesInteractor:
    def __init__(self, expense_repo: ExpenseRepository, user_repo: UserRepository):
        self.expense_repo = expense_repo
        self.user_repo = user_repo

    def execute(self, user_id: int):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        role = user.role
        if not role.can_clear_others_expenses():
            raise PermissionError("User does not have permission to clear others' expenses")
        self.expense_repo.clear(user_id)
