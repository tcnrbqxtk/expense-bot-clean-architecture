from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Expense:
    user_id: int
    amount: float
    category: str
    comment: str = ""
    date: date = field(default_factory=date.today)

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
