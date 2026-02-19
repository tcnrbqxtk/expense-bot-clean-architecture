from dishka import Provider, Scope, provide  # type: ignore

from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository
from domain.repositories.user_settings_repository import UserSettingsRepository
from infrastructure.config import Config
from infrastructure.repositories.json_expense_repository import JsonExpenseRepository
from infrastructure.repositories.json_user_repository import JsonUserRepository
from infrastructure.repositories.json_user_settings_repository import JsonUserSettingsRepository


class RepositoryProvider(Provider):
    scope = Scope.APP

    @provide()
    def provide_expense_repository(
        self,
        config: Config,
    ) -> ExpenseRepository:
        return JsonExpenseRepository(config.EXPENSES_PATH)

    @provide()
    def provide_user_repository(
        self,
        config: Config,
    ) -> UserRepository:
        return JsonUserRepository(config.USERS_PATH)

    @provide()
    def provide_user_settings_repository(
        self,
        config: Config,
    ) -> UserSettingsRepository:
        return JsonUserSettingsRepository(config.USERS_PATH)
