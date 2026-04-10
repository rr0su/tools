"""
shodan_monitor.py
-----------------
Query Shodan for assets related to a domain (by cert CN, hostnames).
Requires SHODAN API key (read-only).
"""

import shodan, json, argparse, os

def query_shodan(api_key, query, out="shodan.json"):
    api = shodan.Shodan(api_key)
    results = api.search(query, limit=100)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print("[+] Saved Shodan results to", out)
    return out

if __name__ == "__main__":
    import sys
    key = os.getenv("SHODAN_KEY")
    if not key:
        print("Set SHODAN_KEY env var.")
        sys.exit(1)
    domain = sys.argv[1] if len(sys.argv)>1 else "example.com"
    q = f"ssl.cert.subject.CN:{domain}"
    query_shodan(key, q, out=f"shodan_{domain}.json")
