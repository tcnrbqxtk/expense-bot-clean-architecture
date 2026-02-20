import json
from typing import Any

from domain.entities.role import Role
from domain.entities.user import User
from domain.entities.user_settings import UserSettings
from domain.repositories.user_repository import UserRepository


class JsonUserRepository(UserRepository):
    def __init__(self, path: str):
        self.path = path

    def _load(self) -> dict[str, dict[str, Any]]:
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save(self, data: dict[str, dict[str, str | float]]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    async def add(self, user: User) -> None:
        data = self._load()
        data[str(user.user_id)] = {
            "role": user.role.name,
            "settings": {"currency": user.settings.currency, "daily_limit": user.settings.daily_limit},
        }
        self._save(data)

    async def get(self, user_id: int) -> User | None:
        data = self._load()
        user_data = data.get(str(user_id))
        if not user_data:
            return None
        role = Role(user_data["role"])
        settings = UserSettings(user_id, **user_data["settings"])
        return User(user_id, role, settings)

    async def exists(self, user_id: int) -> bool:
        data = self._load()
        return str(user_id) in data

    async def save(self, user: User) -> None:
        data = self._load()
        if str(user.user_id) not in data:
            raise ValueError("User not found")
        data[str(user.user_id)] = {
            "role": user.role.name,
            "settings": {"currency": user.settings.currency, "daily_limit": user.settings.daily_limit},
        }
        self._save(data)

    async def count_users(self) -> int:
        data = self._load()
        return len(data)
