from domain.entities.user import Role, User
from domain.repositories.user_repository import UserRepository


class ManageRolesInteractor:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, admin_user: User, target_user_id: int, new_role_name: str):
        if not admin_user.role.can_manage_roles():
            raise PermissionError("User does not have permission to manage roles")

        target_user = self.user_repo.get(target_user_id)
        if not target_user:
            raise ValueError("User not found")

        target_user.role = Role(new_role_name)

        self.user_repo.save(target_user)
