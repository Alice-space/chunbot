from typing import Optional
import requests
from bs4 import BeautifulSoup
from source.base import Source, SourceConfig
import logging

from type import News

logger = logging.getLogger(__name__)


class IHEPEDUSource(Source):
    def __init__(self, config: Optional[SourceConfig] = None):
        super().__init__(config)
        self.config = {"description": "高能物理研究所教育处通知公告"}

    def get_list(self) -> list[News]:
        logger.info("Fetching notice list from IHEP EDU website")
        try:
            resp = requests.get("https://edu1.ihep.ac.cn/tzgg/index.shtml")
            resp.raise_for_status()
            logger.debug(f"Successfully fetched page with status code: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch notices: {str(e)}")
            return [
                {
                    "success": False,
                    "error_msg": str(e),
                    "source": self.config["description"],
                    "importance": "未分配",
                    "summary": None,
                    "title": None,
                    "url": None
                }
            ]
        soup = BeautifulSoup(resp.text, "html.parser")
        news_list: list[News] = []
        list_items = soup.select(".mainListbox .ulList li")
        logger.debug(f"Found {len(list_items)} list items to process")
        for li in list_items:
            a = li.find("a")
            if a is None:
                logger.debug(f"Skipping list item {li} - no anchor tag found")
                continue
            title = a.get_text(strip=True)
            link: str = a.get("href") # type: ignore
            if link.startswith("/"):
                link = "https://edu1.ihep.ac.cn" + link
            news: News = {
                "success": True,
                "source": self.config["description"],
                "title": title,
                "url": link,
                "error_msg": None,
                "importance": "未分配",
                "summary": None
            }
            news_list.append(news)
            logger.debug(f"Added notice: {title}")
        logger.info(f"Successfully fetched {len(news_list)} notices")
        return news_list