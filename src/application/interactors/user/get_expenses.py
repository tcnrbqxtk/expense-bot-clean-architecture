from domain.entities.expense import Expense
from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository


class GetExpensesInteractor:
    def __init__(self, expense_repo: ExpenseRepository, user_repo: UserRepository):
        self.expense_repo = expense_repo
        self.user_repo = user_repo

    def execute(self, user_id: int) -> list[Expense]:
        user = self.user_repo.get(user_id)
        if not user or not user.role.can_view_stats():
            raise PermissionError("User does not have permission to view stats")
        return self.expense_repo.get_expenses_by_user(user_id)
