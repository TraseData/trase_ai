
import os, sys, json, time
LEVELS = {"DEBUG":10,"INFO":20,"WARN":30,"ERROR":40}
LOG_LEVEL = LEVELS.get(os.getenv("LOG_LEVEL","INFO").upper(), 20)
def log(level, msg, **kw):
    if LEVELS.get(level, 99) < LOG_LEVEL: return
    e = {"ts": int(time.time()), "level": level, "msg": msg}
    e.update(kw)
    sys.stdout.write(json.dumps(e, ensure_ascii=False)+"\n"); sys.stdout.flush()
def debug(m, **k): log("DEBUG", m, **k)
def info(m, **k): log("INFO", m, **k)
def warn(m, **k): log("WARN", m, **k)
def error(m, **k): log("ERROR", m, **k)
