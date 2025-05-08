from source.ihep_edu import IHEPEDUSource
from source.base import Source
from store.sqlite import SQLiteStore
from report.terminal import TerminalReporter
from report.base import Reporter
from compile.LLM import LLMCompiler

if __name__ == "__main__":
    sources: list[Source] = [IHEPEDUSource()]
    store = SQLiteStore()
    compiler = LLMCompiler()
    reporters: list[Reporter] = [TerminalReporter()]

    compiled_info = []
    for source in sources:
        source_desp = source.description()
        news = store.update_list(source_desp, source.get_list())
        for title, url in news.items():
            summary_single = compiler.compile_info(source_desp, title, url)
            compiled_info.append((source_desp, title, summary_single, url))
    final_report = compiler.compile_list(compiled_info)
    for reporter in reporters:
        reporter.report(final_report)
