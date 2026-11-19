from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class ShortenRequest(BaseModel):
    long_url:HttpUrl
    expires_at : datetime | None = None
    user_id : int | None = None


class ShortenResponse(BaseModel):
    message:str
    short_code:str
    short_url:str

class UserURLResponse(BaseModel):
    short_code: str
    short_url: str
    long_url: HttpUrl
    total_clicks:int
    created_at: datetime
    expires_at: datetime | None = None
    is_expired : bool


class URLStatsResponse(BaseModel):
    short_code:str
    short_url:str
    total_clicks:int


class UpdateExpirationRequest(BaseModel):
    expires_at: datetime | None = None

class UpdateExpirationResponse(BaseModel):
    message: str
    expires_at: datetime | None



    

