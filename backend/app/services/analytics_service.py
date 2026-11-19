import logging
from fastapi import Depends

from app.repositories.url_click_repository import URLClickRepository, get_url_click_repository
from app.models.url_click_model import URLClick

logger = logging.getLogger(__name__)

class AnalyticsService:

    def __init__(
            self,
            repository:URLClickRepository
    ):
        self.repository = repository

    def record_click(
            self,
            url_id :int,
            ip_address:str,
            user_agent:str,
            referrer:str | None = None
    ) -> None:
        
        # return self.repository.create_click(
        #     url_id=url_id,
        #     ip_address=ip_address,
        #     user_agent=user_agent,
        #     referrer=referrer
        # )

        try:
            self.repository.create_click(
                        url_id=url_id,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        referrer=referrer
                    )
        except Exception:
            logger.exception(
                "Failed to record click"
            )
             

    def get_click_count(
            self,
            url_id:int
    ) -> int:
        return self.repository.get_click_count(url_id=url_id)

    def get_click_counts(
                self,
                url_ids:list[int]
        ) -> dict[int,int]:
            return self.repository.get_click_counts(url_ids=url_ids)


def get_analytics_service(repository:URLClickRepository = Depends(get_url_click_repository)):
    return AnalyticsService(repository)