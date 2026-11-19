from datetime import datetime

from fastapi import Depends
from sqlmodel import Session, select

from app.models.url_model import URL
from app.core.database import get_session


class URLRepository:

    def __init__(self,session: Session):
        self.session = session

    def create_url(self, long_url:str, expires_at: datetime | None = None, user_id:int | None = None) -> URL:

        url = URL(
            long_url=str(long_url),
            short_code="",
            expires_at=expires_at,
            user_id=user_id
        )

        self.session.add(url)
        self.session.flush()


        return url

    def save(self, url: URL) -> URL | None:
        try:
            self.session.commit()
            self.session.refresh(url)
            
            return url
        except Exception:
            self.session.rollback()
            raise 


    def get_by_id(self, id:int) -> URL | None:

        statement = (
            select(URL).where(URL.id == id)
            )

        return self.session.exec(statement).first()


    def get_by_user_id(self, user_id:int) -> list[URL] :
        statement = (
            select(URL)
            .where(URL.user_id == user_id)
            .order_by(URL.created_at.desc())
        )

        return list(
            self.session.exec(statement).all()
        )

    def delete_url(
            self,
            url:URL
    ) -> None:
        try:
            self.session.delete(url)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise



def get_url_repository(
        session: Session = Depends(get_session)
):
    return URLRepository(session)