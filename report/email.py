import datetime
from report.base import Reporter, ReporterConfig
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown

class MailReporterConfig(ReporterConfig):
    smtp_server: str
    smtp_port: int
    sender_email: str
    sender_password: str
    recipient_emails: list[str]


class MailReporter(Reporter):
    def __init__(self, config: MailReporterConfig):
        super().__init__(config)
        self.config: MailReporterConfig = config

    def report(self, compiled_info: str) -> None:
        """Send the compiled info via email"""
        msg = MIMEMultipart()
        msg["From"] = self.config["sender_email"]
        msg["To"] = ", ".join(self.config["recipient_emails"])
        msg["Subject"] = (
            f"今日简报 - {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime('%m月%d日')}"
        )

        html_content = markdown.markdown(compiled_info)
        msg.attach(MIMEText(html_content, "html"))

        try:
            with smtplib.SMTP_SSL(
                self.config["smtp_server"], self.config["smtp_port"]
            ) as server:
                server.login(
                    self.config["sender_email"], self.config["sender_password"]
                )
                server.send_message(msg)
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}")
