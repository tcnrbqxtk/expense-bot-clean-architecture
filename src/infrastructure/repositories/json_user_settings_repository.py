from domain.entities.user_settings import UserSettings
from domain.repositories.user_settings_repository import UserSettingsRepository


class JsonUserSettingsRepository(UserSettingsRepository):
    def __init__(self, path: str):
        self.path = path

    async def get(self, user_id: int) -> UserSettings:
        data = self._load()
        user_data = data.get(str(user_id), {})
        return UserSettings(
            user_id=user_id,
            currency=str(user_data.get("currency", "RUB")),
            daily_limit=float(user_data.get("daily_limit", 0.0)),
        )

    async def save(self, user_settings: UserSettings):
        data = self._load()
        data[str(user_settings.user_id)] = {
            "currency": user_settings.currency,
            "daily_limit": user_settings.daily_limit,
        }
        self._save(data)

    def _load(self) -> dict[str, dict[str, str | float]]:
        import json

        try:
            with open(self.path) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save(self, data: dict[str, dict[str, str | float]]) -> None:
        import json

        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
