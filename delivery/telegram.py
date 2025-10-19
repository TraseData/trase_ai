
import os, requests
from utils.logger import info, error
BOT = os.getenv("TELEGRAM_BOT_TOKEN",""); CHAT=os.getenv("TELEGRAM_CHAT_ID","")
def post(text):
    if not (BOT and CHAT): error("tg.skip", reason="no token/chat"); return False
    r = requests.get(f"https://api.telegram.org/bot{BOT}/sendMessage",
                     params={"chat_id": CHAT, "text": text}, timeout=20)
    if r.status_code >= 300: error("tg.failed", status=r.status_code, text=r.text); return False
    info("tg.ok"); return True
