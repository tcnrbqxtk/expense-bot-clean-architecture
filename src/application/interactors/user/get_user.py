from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class GetUserInteractor:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def __call__(self, user_id: int) -> User | None:
        user = self.user_repo.get(user_id)
        return user
