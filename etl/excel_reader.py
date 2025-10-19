
import os, requests, pandas as pd
from utils.logger import info

AUTH_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
GRAPH = "https://graph.microsoft.com/v1.0"

TENANT_ID = os.environ["MS_TENANT_ID"]
CLIENT_ID = os.environ["MS_CLIENT_ID"]
CLIENT_SECRET = os.environ["MS_CLIENT_SECRET"]
DRIVE_ID = os.environ["CONTROL_DRIVE_ID"]
ITEM_ID = os.environ["CONTROL_ITEM_ID"]
WORKSHEET = os.getenv("CONTROL_WORKSHEET","Control")
TABLE = os.getenv("CONTROL_TABLE","")

def _token():
    r = requests.post(AUTH_URL.format(tenant=TENANT_ID), data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }, timeout=30)
    r.raise_for_status(); return r.json()["access_token"]

def _get(path, token):
    r = requests.get(f"{GRAPH}{path}", headers={"Authorization": f"Bearer {token}"}, timeout=60)
    r.raise_for_status(); return r.json()

def read_excel_df():
    t = _token()
    if TABLE:
        rows = _get(f"/drives/{DRIVE_ID}/items/{ITEM_ID}/workbook/tables('{TABLE}')/rows", t).get("value",[])
        if not rows: return pd.DataFrame()
        data = [r.get("values", [[]])[0] for r in rows]
        cols = _get(f"/drives/{DRIVE_ID}/items/{ITEM_ID}/workbook/tables('{TABLE}')/columns", t).get("value",[])
        headers = [c["name"] for c in cols]
        df = pd.DataFrame(data, columns=headers)
        info("excel.read", source="table", worksheet=WORKSHEET, table=TABLE, rows=len(df)); return df
    used = _get(f"/drives/{DRIVE_ID}/items/{ITEM_ID}/workbook/worksheets('{WORKSHEET}')/usedRange(valuesOnly=true)", t)
    vals = used.get("values", []); 
    if not vals: return pd.DataFrame()
    headers = [str(h).strip() for h in vals[0]]
    df = pd.DataFrame(vals[1:], columns=headers)
    info("excel.read", source="usedRange", worksheet=WORKSHEET, rows=len(df)); return df
