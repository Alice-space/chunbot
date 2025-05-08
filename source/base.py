from abc import ABC, abstractmethod


class Source(ABC):
    # Base of datasource
    def __init__(self, config: dict = None):
        self.config = config or {}

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def get_list(self) -> dict[str, str]:
        # key: title, value: url
        pass
