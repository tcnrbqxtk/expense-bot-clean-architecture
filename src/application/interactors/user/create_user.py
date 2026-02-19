from domain.entities.role import Role
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class CreateUserInteractor:
    def __init__(self, user_repo: UserRepository, admin_ids: list[str]):
        self.user_repo = user_repo
        self.admin_ids = admin_ids

    async def __call__(self, user_id: int):
        if self.user_repo.exists(user_id):
            raise ValueError("Пользователь уже существует")

        role = Role("admin") if str(user_id) in self.admin_ids else Role("user")
        user = User(user_id, role)
        self.user_repo.add(user)
        return user
