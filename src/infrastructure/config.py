from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    EXPENSES_PATH: str = "data/expenses.json"
    USERS_PATH: str = "data/users.json"
    ENV: str = "PROD"
    BOT_TOKEN: str = ""
    ADMIN_IDS: str = ""
    DATA_FILE: str = "data/expenses.json"

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__", case_sensitive=False, extra="allow")

    @property
    def admin_ids_list(self) -> list[str]:
        if not self.ADMIN_IDS:
            return []
        return [id for id in self.ADMIN_IDS.split(",") if id]
