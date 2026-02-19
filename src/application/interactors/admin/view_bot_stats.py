from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository


class ViewBotStatsInteractor:
    def __init__(self, expense_repo: ExpenseRepository, user_repo: UserRepository):
        self.expense_repo = expense_repo
        self.user_repo = user_repo

    def execute(self, user_id: int) -> dict[str, int | float]:
        user = self.user_repo.get(user_id)
        if not user or not user.role.can_view_bot_stats():
            raise PermissionError("Only admins have the permission to view bot stats")
        return {
            "total_sum_of_expenses": self.expense_repo.count_all_expenses(),
            "total_users": self.user_repo.count_users(),
            "total_expenses_count": len(self.expense_repo.get_all_expenses()),
        }
