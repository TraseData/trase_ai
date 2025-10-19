
from fastapi import FastAPI
from pydantic import BaseModel
from run_pipeline import run
from utils.logger import info

app = FastAPI(title="TraseBot — Full System")

class RunReq(BaseModel):
    skip_push: bool = False
    skip_delivery: bool = False
    save_bq: bool = True

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/hooks/control-updated")
def control_updated():
    info("hook.control_updated")
    return run()

@app.post("/run")
def run_now(req: RunReq):
    return run(skip_push=req.skip_push, skip_delivery=req.skip_delivery, save_bq=req.save_bq)
