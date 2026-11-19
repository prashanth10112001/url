from fastapi import Depends
from sqlalchemy import func
from sqlmodel import Session, select

from app.models.url_click_model import URLClick
from app.core.database import get_session


class URLClickRepository:

    def __init__(self, session: Session):
        self.session = session

    def create_click(
            self, 
            url_id:int,
            ip_address:str,
            user_agent:str,
            referrer:str | None = None,
            ) -> URLClick:

        click = URLClick(
            url_id=url_id,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer
        )

        self.session.add(click)
        self.session.commit()
        self.session.refresh(click)


        return click

    def get_clicks_by_url_id(
            self,
            url_id:int
    ) -> list[URLClick]:

        statement = (
            select(URLClick).where(URLClick.url_id == url_id).order_by(URLClick.clicked_at.desc())
        )

        return list(self.session.exec(statement).all())

    def get_click_count(
            self,
            url_id:int
    ) -> int:

        statement = (
            select(func.count()).select_from(URLClick).where(URLClick.url_id == url_id)
        )

        return self.session.exec(statement).one()

    def get_click_counts(
            self,
            url_ids : list[int]
    ) -> dict[int,int]:
        if not url_ids:
            return {}
        statement = (
            select(URLClick.url_id,func.count(URLClick.id)).where(URLClick.url_id.in_(url_ids)).group_by(URLClick.url_id)
        )

        results = self.session.exec(statement).all()

        return {
            url_id:count
            for url_id,count in results
        }

        


def get_url_click_repository( session:Session = Depends(get_session)):
    return URLClickRepository(session)