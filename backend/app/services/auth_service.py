from fastapi import Depends

from app.repositories.user_repository import UserRepository, get_user_repository
from app.models.user_model import User
from app.exceptions.auth_exceptions import EmailAlreadyExists, InvalidCredentials, UsernameAlreadyExists
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token


class AuthService:

    def __init__(self, repository:UserRepository):
        self.repository = repository

    def register_user(self, username:str, email:str,password:str) -> User:


        existing_user = self.repository.get_by_username(username)

        if existing_user:
            raise UsernameAlreadyExists()

        existing_email = self.repository.get_by_email(email)
        
        if existing_email:
            raise EmailAlreadyExists()

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password)
        )

        return self.repository.create_user(user)

    def login_user(self,username:str,password:str) -> str:

        user = self.repository.get_by_username(username)

        if not user:
            raise InvalidCredentials()

        if not verify_password(password,user.password_hash):
            raise InvalidCredentials()

        return create_access_token(user.id)

    



def get_auth_service(repository:UserRepository = Depends(get_user_repository)):
    return AuthService(repository)


