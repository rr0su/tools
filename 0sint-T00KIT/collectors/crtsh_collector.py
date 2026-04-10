"""
crtsh_collector.py
-------------------
Query Certificate Transparency logs (crt.sh) for a domain and extract SANs/subdomain candidates.
Safe & passive (HTTP requests only).
"""

import requests, json, argparse

CRT_URL = "https://crt.sh/?q=%25.{domain}&output=json"

def get_certificates(domain):
    url = CRT_URL.format(domain=domain)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def extract_names(cert_json):
    domains = set()
    for entry in cert_json:
        nv = entry.get("name_value","")
        for d in nv.splitlines():
            domains.add(d.strip())
    return sorted(domains)

def save(domain, out="crtsh.json"):
    j = get_certificates(domain)
    domains = extract_names(j)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"domain": domain, "subdomains": domains}, fh, indent=2)
    print("[+] Saved crtsh results to", out)
    return out

if __name__ == "__main__":
    import sys
    domain = sys.argv[1] if len(sys.argv)>1 else "example.com"
    save(domain, out=f"crtsh_{domain}.json")
