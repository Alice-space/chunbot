from report.base import Reporter, ReporterConfig
from rich.console import Console
from rich.markdown import Markdown


class TerminalReporter(Reporter):
    # Base of datasource
    def __init__(self, config: ReporterConfig | None = None):
        super().__init__(config)
        self.console = Console()

    def report(self, compiled_info: str) -> None:
        md = Markdown(compiled_info)
        self.console.print(md)
