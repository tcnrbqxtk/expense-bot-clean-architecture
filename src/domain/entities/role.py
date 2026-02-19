from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str

    # common permissions for both admin and user
    def can_add(self) -> bool:
        return self.name in ["admin", "user"]

    def can_clear(self) -> bool:
        return self.name in ["admin", "user"]

    def can_view_stats(self) -> bool:
        return self.name in ["admin", "user"]

    def can_update_settings(self) -> bool:
        return self.name in ["admin", "user"]

    # admin-only permissions
    def can_clear_others_expenses(self) -> bool:
        return self.name == "admin"

    def can_manage_roles(self) -> bool:
        return self.name == "admin"

    def can_view_bot_stats(self) -> bool:
        return self.name == "admin"
