from datetime import datetime, timezone

from pydantic import HttpUrl
from sqlmodel import Field, SQLModel


class URL(SQLModel,table=True):
    __tablename__ = "urls"

    id: int | None = Field(primary_key=True,default=None)
    user_id: int | None = Field(default=None, foreign_key="users.id")
    short_code : str = Field(unique=True, index=True)
    long_url : str
    created_at : datetime =  Field(default_factory=lambda:datetime.now(timezone.utc))
    expires_at : datetime | None =  Field(default=None)
