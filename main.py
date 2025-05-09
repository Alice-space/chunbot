from config import Config
from report.email import MailReporter
from source.ihep_edu import IHEPEDUSource
from source.base import Source
from store.sqlite import SQLiteStore
from report.terminal import TerminalReporter
from report.base import Reporter
from compile.LLM import LLMCompiler
import logging

from type import News

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting application")
        sources: list[Source] = [IHEPEDUSource()]
        store = SQLiteStore()
        compiler = LLMCompiler({"personal_info": Config.personal_info})
        reporters: list[Reporter] = [
            TerminalReporter(),
            MailReporter(
                {
                    "recipient_emails": Config.recipient_emails,
                    "sender_email": Config.sender_email,
                    "sender_password": Config.sender_password,
                    "smtp_port": Config.smtp_port,
                    "smtp_server": Config.smtp_server,
                }
            ),
        ]

        compiled_info: list[News] = []
        for source in sources:
            if not source.config:
                logger.warning(f"Skipping source with no config")
                continue
            logger.info(f"Processing source: {source.config['description']}")
            news = store.update_list(source.get_list())
            logger.info(
                f"Found {len(news)} new items from {source.config['description']}"
            )
            for single_news in news:
                logger.debug(f"Processing item: {single_news['title']}")
                result = compiler.compile_info(single_news)
                compiled_info.append(result)
            logger.info(f"Compiled {len(compiled_info)} items total")
        final_report = compiler.compile_list(compiled_info)
        for reporter in reporters:
            reporter.report(final_report)
        logger.info("Application completed successfully")
    except Exception as e:
        logger.error(f"Application failed: {str(e)}", exc_info=True)
