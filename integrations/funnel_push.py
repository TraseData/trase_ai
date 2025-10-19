
import os, requests
from utils.logger import info, error

BASE = os.getenv("FUNNEL_API_BASE","https://api.funnel.io/v1")
KEY = os.getenv("FUNNEL_API_KEY")
DS = os.getenv("FUNNEL_DATA_SOURCE_ID")

def push_rows(rows):
    if not (KEY and DS): raise RuntimeError("Missing FUNNEL_API_KEY or FUNNEL_DATA_SOURCE_ID")
    r = requests.post(f"{BASE}/data-sources/{DS}/data",
                      headers={"Authorization": f"Bearer {KEY}", "Content-Type":"application/json"},
                      json=rows, timeout=90)
    if r.status_code >= 300:
        error("funnel.push.failed", status=r.status_code, text=r.text); r.raise_for_status()
    info("funnel.push.ok", status=r.status_code, count=len(rows))
    return r.status_code
