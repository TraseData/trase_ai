
import pandas as pd
from utils.logger import info

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    rename = {"Date":"date","Source":"source","Campaign":"campaign","Spend":"spend",
              "Impressions":"impressions","Clicks":"clicks","Conversions":"conversions",
              "Revenue":"revenue"}
    df = df.rename(columns={k:v for k,v in rename.items() if k in df.columns})
    if "date" in df.columns: df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    for c in ["spend","impressions","clicks","conversions","revenue"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    if {"clicks","impressions"}.issubset(df.columns):
        df["ctr"] = (df["clicks"]/df["impressions"]).fillna(0)
    if {"revenue","spend"}.issubset(df.columns):
        df["roas"] = (df["revenue"]/df["spend"]).replace([float("inf")],0).fillna(0)
    info("kpi.normalize", rows=len(df)); return df

def to_funnel_schema(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in ["date","source","campaign","spend","impressions","clicks","conversions","revenue","ctr","roas"] if c in df.columns]
    return df[cols]
