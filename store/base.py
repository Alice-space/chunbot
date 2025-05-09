from abc import ABC, abstractmethod
from typing import Optional, TypedDict

from type import News


class StoreConfig(TypedDict, total=False):
    description: str


class Store(ABC):
    # Base of datasource
    def __init__(self, config: Optional[StoreConfig] = None):
        self.config = config or {}

    @abstractmethod
    def update_list(self, news: list[News]) -> list[News]:
        # return new news
        pass
