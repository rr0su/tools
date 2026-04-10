"""
webhook_api.py
--------------
Simple webhook receiver that accepts collector JSON and ingests to Neo4j.
Protect this with auth & IP allowlist in production!
"""

from fastapi import FastAPI, Request, Header, HTTPException
import uvicorn, json, os
from neo4j import GraphDatabase
import requests

app = FastAPI()
conf = json.load(open("config.json"))
driver = GraphDatabase.driver(conf["NEO4J"]["uri"], auth=(conf["NEO4J"]["user"], conf["NEO4J"]["password"]))
SLACK = conf.get("SLACK_WEBHOOK")

def post_slack(text):
    if not SLACK: return
    requests.post(SLACK, json={"text": text})

@app.post("/ingest")
async def ingest(request: Request, x_api_key: str = Header(None)):
    # Basic API key check - replace with HMAC in production
    if x_api_key != os.getenv("INGEST_KEY"):
        raise HTTPException(status_code=403, detail="Forbidden")
    body = await request.json()
    # expected: {"type":"crtsh", "payload": {...}}
    t = body.get("type")
    payload = body.get("payload")
    with driver.session() as s:
        if t == "crtsh":
            domain = payload.get("domain")
            s.run("MERGE (d:Domain {name:$name}) SET d.last_seen = timestamp()", name=domain)
            post_slack(f"New crt.sh data for {domain}")
    return {"status":"ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
