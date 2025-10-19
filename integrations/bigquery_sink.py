
import os, tempfile
from google.cloud import bigquery
from utils.logger import info

PJ = os.getenv("BQ_PROJECT_ID"); DS = os.getenv("BQ_DATASET","trase"); TB = os.getenv("BQ_TABLE","kpi_output")
CREDS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON","")

def _creds():
    if not CREDS: return None
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    f.write(CREDS.encode("utf-8")); f.flush()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name
    return f.name

def append(df):
    if not (PJ and DS and TB): return None
    _creds(); client = bigquery.Client(project=PJ)
    table_id = f"{PJ}.{DS}.{TB}"
    job = client.load_table_from_dataframe(df, table_id, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
    job.result(); info("bq.append.ok", rows=len(df)); return True
