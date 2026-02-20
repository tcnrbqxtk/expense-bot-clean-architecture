from application.services.period import PeriodService
from application.services.stats_formatter import StatsFormatterService

from domain.entities.expense import Expense
from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository


class GetStatsByPeriodInteractor:
    def __init__(
        self,
        user_repo: UserRepository,
        expense_repo: ExpenseRepository,
        period_service: PeriodService,
        stats_formatter_service: StatsFormatterService,
    ) -> None:
        self.user_repo = user_repo
        self.expense_repo = expense_repo
        self.period_service = period_service
        self.stats_formatter_service = stats_formatter_service

    async def __call__(self, user_id: int, period: str = "0") -> str:
        user = await self.user_repo.get(user_id)
        if not user:
            return "Пользователь не найден. Добавьте расход через /add."

        date_floor, date_ceil, period_name = self.period_service(period)

        expenses: list[Expense] = [
            e for e in await self.expense_repo.get_by_user(user_id) if date_floor <= e.date <= date_ceil
        ]

        if not expenses:
            return "Расходов за указанный период не найдено."

        return self.stats_formatter_service(expenses, period_name, user.settings.currency)
