from report.email import MailReporter

def test_get_list():
    r = MailReporter({
        'recipient_emails': [''],
        'sender_email': '',
        'sender_password': '',
        'smtp_port': 465,
        'smtp_server': '',
    })
    r.report("test")