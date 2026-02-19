from domain.repositories.user_settings_repository import UserSettingsRepository


class GetUserSettingsInfoInteractor:
    def __init__(self, user_settings_repo: UserSettingsRepository):
        self.user_settings_repo = user_settings_repo

    async def __call__(self, user_id: int) -> str:
        settings = self.user_settings_repo.get(user_id)
        currency = getattr(settings, "currency", "RUB")
        daily_limit = getattr(settings, "daily_limit", 0)

        return (
            "<b>⚙️ Настройки бота:</b>\n\n"
            "Здесь вы можете изменить настройки бота.\n\n"
            "<i>Доступные настройки:</i>\n"
            "<pre>"
            f"1) Валюта (текущая: {currency})\n"
            f"2) Дневной Лимит (текущий: {daily_limit})\n"
            "</pre>"
            "/quit - Выйти из меню настроек"
        )
