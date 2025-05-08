from abc import ABC, abstractmethod


class Store(ABC):
    # Base of datasource
    def __init__(self, config: dict = None):
        self.config = config or {}

    @abstractmethod
    def update_list(
        self, source_description: str, news: dict[str, str]
    ) -> dict[str, str]:
        # key: title, value: url, which is new
        pass
