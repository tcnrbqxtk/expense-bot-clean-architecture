from typing import Protocol

from domain.entities.user_settings import UserSettings


class UserSettingsRepository(Protocol):
    def get_settings_by_user(self, user_id: int) -> UserSettings:
        """Get user settings"""
        return UserSettings(user_id)

    def save_settings(self, user_settings: UserSettings):
        """Save user settings"""
        ...
