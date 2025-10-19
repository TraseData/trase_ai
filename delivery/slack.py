
import os, requests
from utils.logger import info, error
URL = os.getenv("SLACK_WEBHOOK_URL","")
def post(text):
    if not URL: error("slack.skip", reason="no webhook"); return False
    r = requests.post(URL, json={"text": text}, timeout=20)
    if r.status_code >= 300: error("slack.failed", status=r.status_code, text=r.text); return False
    info("slack.ok"); return True
