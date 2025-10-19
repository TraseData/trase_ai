
import os, requests
from utils.logger import info, error
URL = os.getenv("DISCORD_WEBHOOK_URL","")
def post(text):
    if not URL: error("discord.skip", reason="no webhook"); return False
    r = requests.post(URL, json={"content": text}, timeout=20)
    if r.status_code >= 300: error("discord.failed", status=r.status_code, text=r.text); return False
    info("discord.ok"); return True
