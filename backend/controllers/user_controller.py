# backend/controllers/user_controller.py

import jwt
from backend.repositories.user_repository import UserRepository
from backend.utils.config import Config
from passlib.hash import bcrypt

class UserController:
    @staticmethod
    def register(username, password, role):
        if UserRepository.get_by_username(username):
            raise ValueError("El usuario ya existe.")
        hashed_password = bcrypt.hash(password)
        return UserRepository.create(username, hashed_password, role)

    @staticmethod
    def authenticate(username, password):
        user = UserRepository.get_by_username(username)
        if user and bcrypt.verify(password, user.password):
            return user
        return None

    @staticmethod
    def login(username, password):
        """
        Intenta autenticar y, si tiene éxito,
        devuelve un token JWT con user_id, username y role.
        """
        user = UserController.authenticate(username, password)
        if not user:
            return None
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def list_users():
        return UserRepository.get_all()

    @staticmethod
    def delete_user(user_id):
        return UserRepository.delete(user_id)
