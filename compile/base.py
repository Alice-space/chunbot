from abc import ABC, abstractmethod
from typing import Optional, TypedDict

from type import News


class CompilerConfig(TypedDict):
    pass


class Compiler(ABC):
    # Base of datasource
    def __init__(self, config: Optional[CompilerConfig] = None):
        self.config = config

    @abstractmethod
    def compile_info(self, news: News) -> News:
        # key: title, value: url
        # return report passage, importance
        pass

    @abstractmethod
    def compile_list(self, news: list[News]) -> str:
        pass
