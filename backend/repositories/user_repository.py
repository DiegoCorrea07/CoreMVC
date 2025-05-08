
from backend.models.user import User

class UserRepository:
    @staticmethod
    def create(username, password, role):
        return User.create(username=username, password=password, role=role)

    @staticmethod
    def get_by_username(username):
        return User.get_or_none(User.username == username)

    @staticmethod
    def get_all():
        return list(User.select())

    @staticmethod
    def delete(user_id):
        user = User.get_or_none(User.id == user_id)
        if user:
            user.delete_instance()
            return True
        return False
