from dataclasses import dataclass


@dataclass
class UserSettings:
    user_id: int
    currency: str = "RUB"
    daily_limit: float = 0.0

    def set_currency(self, currency: str):
        if currency not in ["RUB", "USD", "EUR"]:
            raise ValueError("Неверная валюта")
        self.currency = currency

    def set_daily_limit(self, amount: float):
        if amount < 0:
            raise ValueError("Лимит не может быть отрицательным")
        self.daily_limit = amount
