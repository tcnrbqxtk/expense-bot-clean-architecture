from domain.repositories.user_settings_repository import UserSettingsRepository


class ChangeCurrencyInteractor:
    def __init__(self, repo: UserSettingsRepository) -> None:
        self.repo = repo

    async def __call__(self, user_id: int, currency: str) -> None:
        settings = await self.repo.get(user_id)
        settings.currency = currency
        await self.repo.save(settings)
