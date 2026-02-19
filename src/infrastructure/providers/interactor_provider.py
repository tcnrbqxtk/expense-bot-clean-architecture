from dishka import Provider, Scope, provide  # type: ignore
from application.interactors.user.add_expense import AddExpenseInteractor
from application.interactors.user.create_user import CreateUserInteractor
from application.interactors.user.get_expenses import GetExpensesInteractor
from application.interactors.user.get_user import GetUserInteractor
from domain.repositories.expense_repository import ExpenseRepository
from domain.repositories.user_repository import UserRepository


class InteractorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_add_expense(
        self,
        expense_repo: ExpenseRepository,
    ) -> AddExpenseInteractor:
        return AddExpenseInteractor(expense_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_expenses(
        self,
        expense_repo: ExpenseRepository,
        user_repo: UserRepository
    ) -> GetExpensesInteractor:
        return GetExpensesInteractor(expense_repo, user_repo)
    
    @provide(scope=Scope.REQUEST)
    async def provide_create_user_interactor(
        self, user_repo: UserRepository, admin_ids: list[str]
    ) -> CreateUserInteractor:
        return CreateUserInteractor(user_repo, admin_ids)
    
    @provide(scope=Scope.REQUEST)
    async def provide_get_user_interactor(
        self, user_repo: UserRepository
    ) -> GetUserInteractor:
        return GetUserInteractor(user_repo)