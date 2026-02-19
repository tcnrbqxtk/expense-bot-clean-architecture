from domain.repositories.user_settings_repository import UserSettingsRepository


class UpdateSettingsInteractor:
    def __init__(self, repo: UserSettingsRepository):
        self.repo = repo

    def change_currency(self, user_id: int, currency: str):
        settings = self.repo.get_settings_by_user(user_id)
        settings.currency = currency
        self.repo.save_settings(settings)

    def change_daily_limit(self, user_id: int, daily_limit: float):
        settings = self.repo.get_settings_by_user(user_id)
        settings.daily_limit = daily_limit
        self.repo.save_settings(settings)
