from abc import ABC, abstractmethod
from typing import Optional, TypedDict


class ReporterConfig(TypedDict):
    pass


class Reporter(ABC):
    # Base of datasource
    def __init__(self, config: Optional[ReporterConfig] = None):
        self.config = config or {}

    @abstractmethod
    def report(self, compiled_info: str) -> None:
        pass
