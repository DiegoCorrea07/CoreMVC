import jwt
from passlib.hash import bcrypt


class UserController:
    """
    Controlador para orquestar las operaciones de los Usuarios, incluyendo
    autenticación y generación de tokens.
    Recibe un repositorio y la configuración a través de inyección de dependencias.
    """

    # 1. Modificamos el constructor para recibir el repositorio y la clave secreta.
    def __init__(self, repository, secret_key):
        self.repository = repository
        self.secret_key = secret_key

    # 2. Quitamos @staticmethod y usamos 'self'.
    def register(self, username, password, role):
        # La lógica de negocio (validaciones, hashing) permanece en el controlador.
        if self.repository.get_by_username(username):
            raise ValueError("El usuario ya existe.")

        hashed_password = bcrypt.hash(password)
        return self.repository.create(username, hashed_password, role)

    def authenticate(self, username, password):
        user = self.repository.get_by_username(username)
        if user and bcrypt.verify(password, user.password):
            return user
        return None

    def login(self, username, password):
        """
        Intenta autenticar y, si tiene éxito,
        devuelve un token JWT con user_id, username y role.
        """
        # La llamada interna ahora usa 'self'.
        user = self.authenticate(username, password)
        if not user:
            return None

        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def get_user(self, user_id):
        return self.repository.get_by_id(user_id)

    def list_users(self):
        return self.repository.get_all()

    def delete_user(self, user_id):
        return self.repository.delete(user_id)
