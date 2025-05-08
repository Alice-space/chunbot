from source.ihep_edu import IHEPEDUSource
from source.base import Source
from store.sqlite import SQLiteStore
from report.terminal import TerminalReporter
from report.base import Reporter
from compile.LLM import LLMCompiler


sources: list[Source] = [IHEPEDUSource()]
store = SQLiteStore()
compiler = LLMCompiler()
reporters: list[Reporter] = [TerminalReporter()]


compiled_info: list[tuple[str, str, str]] = []
for source in sources:
    news = store.update_list(source.description(), source.get_list())
    print(news)
    for title, url in news.items():
        detail = source.get_detail(url)
        summary_single = compiler.compile_info(source.description(), title, detail)
        compiled_info.append((source.description(), title, summary_single))
final_report = compiler.compile_list(compiled_info)
for reporter in reporters:
    reporter.report(final_report)
