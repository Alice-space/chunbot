from report.base import Reporter


class TerminalReporter(Reporter):
    # Base of datasource
    def __init__(self, config: dict = None):
        self.config = config or {}

    def report(self, compiled_info: str) -> None:
        print(compiled_info)
