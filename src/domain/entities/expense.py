from dataclasses import dataclass


@dataclass(frozen=True)
class Expense:
    user_id: int
    amount: float
    category: str
    comment: str = ""

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
