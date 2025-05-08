from abc import ABC, abstractmethod

class Reporter(ABC):
    # Base of datasource
    def __init__(self, config: dict = None):
        self.config = config or {}

    @abstractmethod
    def report(self, compiled_info: str) -> None:
        # key: title, value: url
        # return report passage
        pass