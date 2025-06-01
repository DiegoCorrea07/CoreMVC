import jwt
from functools import wraps
from backend.utils.config import Config
from backend.utils.permissions import ROLES_PERMISOS


def authenticated_user(method):
    """
    Decorador para métodos de RequestHandler que verifica la autenticación JWT.
    """
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        auth_header = self.request.headers.get("Authorization")
        if not auth_header:
            self.set_status(401)
            self.write({"message": "No autorizado: Token no proporcionado."})
            return

        try:
            token_type, token = auth_header.split(" ")
            if token_type != "Bearer":
                raise ValueError("Tipo de token inválido.")

            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])

            self.current_user = decoded_token

            await method(self, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            self.set_status(401)
            self.write({"message": "No autorizado: Token expirado."})
        except jwt.InvalidTokenError:
            self.set_status(401)
            self.write({"message": "No autorizado: Token inválido."})
        except ValueError as ve:
            self.set_status(401)
            self.write({"message": f"No autorizado: {str(ve)}"})
        except Exception as e:
            self.set_status(500)
            self.write({"message": f"Error interno de autenticación: {str(e)}"})

    return wrapper

def require_permission(permission_name):
    def decorator(method):
        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            user = getattr(self, 'current_user', None)

            if not user:
                self.set_status(401)
                self.write({"message": "No autorizado: Usuario no autenticado."})
                return

            role = user.get("role")

            allowed_permissions = ROLES_PERMISOS.get(role, [])

            if permission_name not in allowed_permissions:
                self.set_status(403)
                self.write({"message": f"Acceso denegado: Se requiere permiso '{permission_name}'."})
                return

            return await method(self, *args, **kwargs)
        return wrapper
    return decorator