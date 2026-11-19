from fastapi import Depends

from app.repositories.user_repository import UserRepository, get_user_repository
from app.models.user_model import User
from app.exceptions.auth_exceptions import EmailAlreadyExists, InvalidCredentials, UsernameAlreadyExists
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.logging.logger import get_logger

logger = get_logger(__name__)


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

        # return self.repository.create_user(user)
        created_user = self.repository.create_user(user)

        logger.info(
            "USER_REGISTERED | user=%s",
            username
        )

        return created_user

    def login_user(self,username:str,password:str) -> str:

        user = self.repository.get_by_username(username)

        if not user or not verify_password(password,user.password_hash):
            logger.warning(
                "LOGIN_FAILED | user=%s",
                username
            )
            raise InvalidCredentials()

        logger.info(
            "LOGIN_SUCCESS | user=%s",
            username
        )

        return create_access_token(user.id)

    



def get_auth_service(repository:UserRepository = Depends(get_user_repository)):
    return AuthService(repository)


