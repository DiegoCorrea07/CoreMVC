from backend.models.user import User

class UserRepository:
    """
    Repositorio para gestionar las operaciones de la base de datos para los Usuarios.
    Los métodos son de instancia para permitir la Inyección de Dependencias.
    """

    # SE ELIMINA @staticmethod
    def create(self, username, password, role):
        # La lógica de hashing de la contraseña debería estar en el controlador/servicio,
        # pero para esta refactorización, mantenemos la estructura.
        return User.create(username=username, password=password, role=role)

    # SE ELIMINA @staticmethod
    def get_by_username(self, username):
        return User.get_or_none(User.username == username)

    def get_by_id(self, user_id):
        return User.get_or_none(User.id == user_id)

    # SE ELIMINA @staticmethod
    def get_all(self):
        return list(User.select())

    # SE ELIMINA @staticmethod
    def delete(self, user_id):
        user = User.get_or_none(User.id == user_id)
        if user:
            user.delete_instance()
            return True
        return False
