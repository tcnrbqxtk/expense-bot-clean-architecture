from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository


class ClearExpensesInteractor:
    def __init__(self, expense_repo: ExpenseRepository, user_repo: UserRepository):
        self.expense_repo = expense_repo
        self.user_repo = user_repo

    def execute(self, user_id: int):
        user = self.user_repo.get(user_id)
        if not user or not user.role.can_clear_expenses():
            raise PermissionError("User does not have permission to clear expenses")
        self.expense_repo.clear_expenses(user_id)
