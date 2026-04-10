"""
neo4j_ingest.py
----------------
Takes JSON outputs from collectors and creates typed nodes/relations.
This is the "brain" ingestion that normalizes data for queries/visuals.
"""

import json, os
from neo4j import GraphDatabase

conf = json.load(open("config.json"))
uri = conf["NEO4J"]["uri"]
user = conf["NEO4J"]["user"]
pw = conf["NEO4J"]["password"]
driver = GraphDatabase.driver(uri, auth=(user, pw))

def add_domain(tx, domain):
    tx.run("MERGE (d:Domain {name:$name}) SET d.last_seen = timestamp()", name=domain)

def add_email(tx, email, domain=None):
    tx.run("MERGE (e:Email {value:$email}) SET e.last_seen = timestamp()", email=email)
    if domain:
        tx.run("MERGE (d:Domain {name:$domain}) MERGE (e)-[:BELONGS_TO]->(d)", domain=domain)

def ingest_crtsh(path):
    j = json.load(open(path))
    domain = j.get("domain")
    subs = j.get("subdomains", [])
    with driver.session() as s:
        add_domain(s, domain)
        for sub in subs:
            s.run("MERGE (s:Subdomain {name:$name}) MERGE (d:Domain {name:$domain}) MERGE (s)-[:CHILD_OF]->(d)",
                  name=sub, domain=domain)

def ingest_pdf_meta(path):
    j = json.load(open(path))
    with driver.session() as s:
        for rec in j:
            meta = rec.get("meta", {})
            # Try to find email/author fields in metadata
            author = meta.get("Author") or meta.get("Creator") or meta.get("Producer")
            if author:
                s.run("MERGE (p:Person {name:$name}) SET p.last_seen = timestamp()", name=author)

if __name__ == "__main__":
    # Example usage:
    if os.path.exists("crtsh_example.com.json"):
        ingest_crtsh("crtsh_example.com.json")
    if os.path.exists("pdf_metadata.json"):
        ingest_pdf_meta("pdf_metadata.json")
    print("[+] Neo4j ingestion complete")
