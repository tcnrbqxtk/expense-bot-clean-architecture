from dishka import Provider, Scope, provide  # type: ignore

from application.interactors.user.add_expense import AddExpenseInteractor
from application.interactors.user.add_expense_for_user import GetOrCreateUserAndAddExpenseInteractor
from application.interactors.user.change_currency import ChangeCurrencyInteractor
from application.interactors.user.change_daily_limit import ChangeDailyLimitInteractor
from application.interactors.user.create_user import CreateUserInteractor
from application.interactors.user.get_expenses import GetExpensesInteractor
from application.interactors.user.get_stats_by_period import GetStatsByPeriodInteractor
from application.interactors.user.get_user import GetUserInteractor
from application.interactors.user.get_user_settings import GetUserSettingsInfoInteractor
from application.services.period import PeriodService
from application.services.stats_formatter import StatsFormatterService
from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository
from domain.repositories.user_settings_repository import UserSettingsRepository


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_add_expense(
        self,
        expense_repo: ExpenseRepository,
    ) -> AddExpenseInteractor:
        return AddExpenseInteractor(expense_repo)

    @provide
    def provide_get_expenses(self, expense_repo: ExpenseRepository, user_repo: UserRepository) -> GetExpensesInteractor:
        return GetExpensesInteractor(expense_repo, user_repo)

    @provide
    async def provide_create_user_interactor(
        self, user_repo: UserRepository, admin_ids: list[str]
    ) -> CreateUserInteractor:
        return CreateUserInteractor(user_repo, admin_ids)

    @provide
    async def provide_get_or_create_and_add_expense_interactor(
        self, user_repo: UserRepository, expense_repo: ExpenseRepository, admin_ids: list[str]
    ) -> GetOrCreateUserAndAddExpenseInteractor:
        return GetOrCreateUserAndAddExpenseInteractor(user_repo, expense_repo, admin_ids)

    @provide
    async def provide_get_user_interactor(self, user_repo: UserRepository) -> GetUserInteractor:
        return GetUserInteractor(user_repo)

    @provide
    async def provide_change_daily_limit_interactor(
        self, user_settings_repo: UserSettingsRepository
    ) -> ChangeDailyLimitInteractor:
        return ChangeDailyLimitInteractor(user_settings_repo)

    @provide
    async def provide_change_currency_interactor(
        self, user_settings_repo: UserSettingsRepository
    ) -> ChangeCurrencyInteractor:
        return ChangeCurrencyInteractor(user_settings_repo)

    @provide
    async def provide_get_user_settings_interactor(
        self, user_settings_repo: UserSettingsRepository
    ) -> GetUserSettingsInfoInteractor:
        return GetUserSettingsInfoInteractor(user_settings_repo)

    @provide
    async def provide_get_stats_by_period_interactor(
        self,
        user_repo: UserRepository,
        expense_repo: ExpenseRepository,
        period_service: PeriodService,
        stats_formatter_service: StatsFormatterService,
    ) -> GetStatsByPeriodInteractor:
        return GetStatsByPeriodInteractor(user_repo, expense_repo, period_service, stats_formatter_service)
