from typing import Protocol

from domain.entities.user_settings import UserSettings


class UserSettingsRepository(Protocol):
    async def get(self, user_id: int) -> UserSettings:
        """Get user settings"""
        return UserSettings(user_id)

    async def save(self, user_settings: UserSettings):
        """Save user settings"""
        ...
