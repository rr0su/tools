"""
github_monitor.py
-----------------
Monitor public GitHub repositories for a target org/user via GitHub Search API.
This script is rate-limited by GitHub; it must use auth to raise limits.
It looks for sensitive keywords in code/commits and records findings.
"""

import requests, json, argparse, os, time
from datetime import datetime

BASE = "https://api.github.com"

def search_code(token, query, per_page=30):
    headers = {"Authorization": f"token {token}"} if token else {}
    url = f"{BASE}/search/code"
    params = {"q": query, "per_page": per_page}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def scan_org_repos(token, org, keywords=None, out="github_findings.json"):
    if keywords is None:
        keywords = ["password", "aws_access_key_id", "secret", "API_KEY", "token"]
    findings = []
    for kw in keywords:
        q = f"user:{org} {kw} in:file"
        try:
            res = search_code(token, q)
            items = res.get("items", [])
            for it in items:
                findings.append({
                    "keyword": kw,
                    "path": it.get("path"),
                    "repository": it.get("repository", {}).get("full_name"),
                    "url": it.get("html_url"),
                    "timestamp": datetime.utcnow().isoformat()
                })
        except Exception as e:
            print("[-] GitHub query error:", e)
            time.sleep(2)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(findings, fh, indent=2)
    print("[+] Saved GitHub findings to", out)
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--org", required=True)
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN"))
    parser.add_argument("--out", default="github_findings.json")
    args = parser.parse_args()
    scan_org_repos(args.token, args.org, out=args.out)
