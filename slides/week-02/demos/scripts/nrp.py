"""Minimal NRP client for the Week 2 demos. The key is read from NRP_LLM_API_KEY and never written anywhere."""
import json
import os
import pathlib
import time

import requests

BASE = "https://ellm.nrp-nautilus.io/v1"
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
PROMPTS = ROOT / "prompts"
RAW.mkdir(exist_ok=True)
PROMPTS.mkdir(exist_ok=True)


def _headers():
    return {"Authorization": f"Bearer {os.environ['NRP_LLM_API_KEY']}", "Content-Type": "application/json"}


def post(path, body, raw_name, timeout=600):
    """POST to the API, save {request, response, latency_s, http_status} to raw/<raw_name>.json."""
    t0 = time.time()
    r = requests.post(f"{BASE}{path}", headers=_headers(), json=body, timeout=timeout)
    dt = time.time() - t0
    try:
        resp = r.json()
    except ValueError:
        resp = {"non_json_body": r.text[:2000]}
    rec = {"endpoint": path, "http_status": r.status_code, "latency_s": round(dt, 2), "request": body, "response": resp}
    (RAW / f"{raw_name}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    return rec


def chat(model, messages, raw_name, **params):
    body = {"model": model, "messages": messages, "temperature": 0, **params}
    return post("/chat/completions", body, raw_name)


def answer_text(rec):
    try:
        return rec["response"]["choices"][0]["message"].get("content") or ""
    except (KeyError, IndexError, TypeError):
        return ""


def usage(rec):
    u = (rec.get("response") or {}).get("usage") or {}
    det = u.get("completion_tokens_details") or {}
    return {
        "prompt_tokens": u.get("prompt_tokens"),
        "completion_tokens": u.get("completion_tokens"),
        "reasoning_tokens": det.get("reasoning_tokens"),
    }


def save_prompt(name, text):
    (PROMPTS / name).write_text(text)
