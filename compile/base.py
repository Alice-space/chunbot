from abc import ABC, abstractmethod

class Compiler(ABC):
    # Base of datasource
    def __init__(self, config: dict = None):
        self.config = config or {}

    @abstractmethod
    def compile_info(self, source_description: str, title: str, detail: str) -> str:
        # key: title, value: url
        # return report passage
        pass

    @abstractmethod
    def compile_list(self, info_list: list[tuple[str, str, str]]) -> str:
        # source, title, summary
        pass