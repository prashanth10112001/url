from datetime import datetime, timezone

from fastapi import Depends

from app.utils.base62 import decode, encode, generate_id
from app.repositories.url_repository import URLRepository, get_url_repository
from app.exceptions.url_exceptions import URLAccessDenied, URLExpired, URLNotFound
from app.models.url_model import URL
from app.repositories.cache_repositories import CacheRepository, get_cache_repository


class URLService:

    def __init__(self, repository: URLRepository, cache_repository:CacheRepository):
        self.repository = repository
        self.cache_repository = cache_repository

    def create_short_url(self,long_url:str, expires_at: datetime | None = None, user_id:int | None = None)->str:

        url = self.repository.create_url(long_url,expires_at=expires_at,user_id=user_id)
        
        url.short_code = encode(url.id)
    
        self.repository.save(url)
    
        return url.short_code

    def get_original_url(self,code:str)->URL:

        cached_url = self.cache_repository.get(code)

        if cached_url is not None:
             return URL(
                  id=cached_url["id"],
                  long_url=cached_url["long_url"],
                  short_code=code
             )



        id = int(decode(code))
        url = self.repository.get_by_id(id)

        if not url:
                raise URLNotFound()

        now = datetime.now(timezone.utc)
        
        if (url.expires_at and now >= url.expires_at):
            raise URLExpired()

        ttl = 300

        if url.expires_at:
            remaining_seconds = int( ( url.expires_at - now).total_seconds())
            ttl = min(ttl,remaining_seconds)

        if ttl > 0:
            self.cache_repository.set(
                key=code,
                value={
                     "id":url.id,
                     "long_url":str(url.long_url)
                },
                ttl=ttl
            )

        return url

    def get_user_urls(self, user_id:int) -> list[URL]:
         return self.repository.get_by_user_id(user_id)


    def get_url(self,code:str) -> URL:

        url_id = int(decode(code))
        url = self.repository.get_by_id(url_id)
        if not url:
             raise URLNotFound()

        return url

    def delete_url(
              self,
              code:str,
              current_user_id:int
    ) -> None:
        url = self.get_url(code)

        if url.user_id != current_user_id:
             raise URLAccessDenied()

        self.repository.delete_url(url)

        self.cache_repository.delete(code)

    def update_expiration(
        self,
        code:str,
        current_user_id:int,
        expires_at:datetime | None
    ) -> URL:
        url = self.get_url(code)

        if url.user_id != current_user_id:
            raise URLAccessDenied()

        url.expires_at = expires_at

        self.repository.save(url)
        self.cache_repository.delete(code)
        return url

         
         




def get_url_service(
        repository : URLRepository = Depends(get_url_repository),
        cache_repository:CacheRepository = Depends(get_cache_repository)
):
    return URLService(repository, cache_repository)