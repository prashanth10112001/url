from fastapi import Depends
from sqlmodel import Session, select

from app.models.user_model import User
from app.core.database import get_session


class UserRepository:

    def __init__(self,session:Session):
        self.session = session

    def create_user(self, user:User) -> User:

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_by_username(self, username:str) -> User | None:
        statement = (
            select(User).where(User.username == username)
        )

        return self.session.exec(statement).first()

    def get_by_email(self, email:str) -> User | None:
        statement = (
            select(User).where(User.email == email)
        )
    
        return self.session.exec(statement).first()

    def get_by_id(self, id:int) -> User | None:
        statement = (
            select(User).where(User.id == id)
        )
    
        return self.session.exec(statement).first()



def get_user_repository(session:Session = Depends(get_session)):
    return UserRepository(session)
        



        