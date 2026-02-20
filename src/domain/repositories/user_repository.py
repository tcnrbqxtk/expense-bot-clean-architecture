from typing import Protocol

from domain.entities.user import User


class UserRepository(Protocol):
    async def save(self, user: User) -> None:
        """Save user to repository"""
        ...

    async def add(self, user: User) -> None:
        """Make a new user"""
        ...

    async def get(self, user_id: int) -> User | None:
        """Returns User by user_id or None if not found"""
        ...

    async def exists(self, user_id: int) -> bool:
        """Checks, if user exists in repository"""
        ...

    async def count_users(self) -> int:
        """Returns the number of users in the repository"""
        ...
