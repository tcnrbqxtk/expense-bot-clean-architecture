from domain.repositories.user_settings_repository import UserSettingsRepository


class ChangeDailyLimitInteractor:
    def __init__(self, repo: UserSettingsRepository) -> None:
        self.repo = repo

    async def __call__(self, user_id: int, daily_limit: int) -> None:
        settings = await self.repo.get(user_id)
        settings.daily_limit = daily_limit
        await self.repo.save(settings)
