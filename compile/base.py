from abc import ABC, abstractmethod
import requests


class Compiler(ABC):
    # Base of datasource
    def __init__(self, config: dict = None):
        self.config = config or {}

    @abstractmethod
    def compile_info(self, source_description: str, title: str, url: str) -> tuple[str, str]:
        # key: title, value: url
        # return report passage, importance
        pass

    @abstractmethod
    def compile_list(self, info_list: list[tuple[str, str, str]]) -> str:
        # source, title, summary
        pass

    def get_info(self, url: str) -> str:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.text
