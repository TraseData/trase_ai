
import os, smtplib
from email.mime.text import MIMEText
from utils.logger import info, error

HOST = os.getenv("SMTP_HOST"); PORT = int(os.getenv("SMTP_PORT","587"))
USER = os.getenv("SMTP_USER"); PASS = os.getenv("SMTP_PASS")
MAIL_FROM = os.getenv("MAIL_FROM","TraseBot <no-reply@trasebot.local>")
MAIL_TO = os.getenv("MAIL_TO","client@example.com")

def send_email(subject, body):
    if not (HOST and USER and PASS):
        error("email.skip", reason="SMTP creds missing"); return False
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject; msg["From"] = MAIL_FROM; msg["To"] = MAIL_TO
    with smtplib.SMTP(HOST, PORT) as s:
        s.starttls(); s.login(USER, PASS); s.sendmail(MAIL_FROM, [MAIL_TO], msg.as_string())
    info("email.sent", to=MAIL_TO); return True
