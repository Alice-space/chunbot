from abc import ABC, abstractmethod
from type import News
from typing import Optional, TypedDict


class SourceConfig(TypedDict):
    description: str


class Source(ABC):
    # Base of datasource
    def __init__(self, config: Optional[SourceConfig] = None):
        self.config = config

    @abstractmethod
    def get_list(self) -> list[News]:
        pass
