from dataclasses import dataclass, field

from domain.entities.role import Role
from domain.entities.user_settings import UserSettings


@dataclass
class User:
    user_id: int
    role: Role = field(default_factory=lambda: Role("user"))
    settings: UserSettings = field(default_factory=lambda: UserSettings(0))

    def __post_init__(self):
        # if settings were created with user_id=0 via default_factory, replace with correct one
        if self.settings.user_id == 0:
            self.settings = UserSettings(self.user_id)
