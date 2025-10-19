
from utils.logger import info, error
from etl.excel_reader import read_excel_df
from etl.kpi import normalize, to_funnel_schema
from integrations.funnel_push import push_rows
from integrations.bigquery_sink import append
from insights.engine import generate_insights
from delivery.emailer import send_email
from delivery.slack import post as slack_post
from delivery.discord import post as discord_post
from delivery.telegram import post as tg_post

def run(skip_push=False, skip_delivery=False, save_bq=True):
    df = read_excel_df()
    if df.empty: info("run.empty"); return {"pushed":0,"delivered":False}
    df = normalize(df)
    funnel_df = to_funnel_schema(df)
    rows = funnel_df.to_dict(orient="records")
    pushed = 0
    if not skip_push:
        push_rows(rows); pushed = len(rows)
    if save_bq:
        try: append(funnel_df)
        except Exception as e: error("bq.err", err=str(e))
    text = generate_insights(funnel_df)
    delivered = False
    if not skip_delivery:
        delivered = any([
            send_email("TraseBot Daily Insights", text),
            slack_post(text),
            discord_post(text),
            tg_post(text),
        ])
    info("run.done", pushed=pushed, delivered=delivered)
    return {"pushed": pushed, "delivered": delivered}

if __name__ == "__main__":
    run()
