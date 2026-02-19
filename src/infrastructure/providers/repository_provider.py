from dishka import Provider, Scope, provide  # type: ignore
from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.json_expense_repository import JsonExpenseRepository

from infrastructure.config import Config
from infrastructure.repositories.json_user_repository import JsonUserRepository


class RepositoryProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_expense_repository(
        self,
        config: Config,
    ) -> ExpenseRepository:
        return JsonExpenseRepository(config.EXPENSES_PATH)

    @provide(scope=Scope.APP)
    def provide_user_repository(
        self,
        config: Config,
    ) -> UserRepository:
        return JsonUserRepository(config.USERS_PATH)
