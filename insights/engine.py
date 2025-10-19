
import os, pandas as pd
from utils.logger import info

def generate_insights(df: pd.DataFrame) -> str:
    lines = []
    total_spend = df.get("spend", pd.Series()).sum() if "spend" in df.columns else 0
    total_rev = df.get("revenue", pd.Series()).sum() if "revenue" in df.columns else 0
    avg_roas = (df["roas"].mean() if "roas" in df.columns and len(df) else 0)
    lines.append(f"Total Spend: {total_spend:,.2f}")
    lines.append(f"Total Revenue: {total_rev:,.2f}")
    lines.append(f"Average ROAS: {avg_roas:,.2f}")
    if "campaign" in df.columns and "roas" in df.columns:
        top = df.groupby("campaign")["roas"].mean().sort_values(ascending=False).head(3)
        if len(top):
            lines.append("Top Campaigns by ROAS:")
            for k,v in top.items():
                lines.append(f"  • {k}: {v:,.2f}")
    info("insights.generated")
    return "\n".join(lines)
