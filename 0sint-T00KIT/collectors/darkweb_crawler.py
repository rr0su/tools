"""
darkweb_crawler.py
------------------
Light Tor-based crawler to fetch .onion pages. DOES NOT auto-download attachments.
Requires tor running locally (socks5 proxy).
This script is read-only: fetch & save HTML for later parsing.
"""

import requests, json, argparse, os
from bs4 import BeautifulSoup

def fetch_onion(url, socks_proxy="socks5h://127.0.0.1:9050", timeout=30):
    s = requests.Session()
    s.proxies = {"http": socks_proxy, "https": socks_proxy}
    r = s.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text

def crawl_list(onion_list_file, out="darkweb_pages.json"):
    results = []
    with open(onion_list_file) as fh:
        for line in fh:
            url = line.strip()
            try:
                html = fetch_onion(url)
                title = BeautifulSoup(html, "html.parser").title.string if html else ""
                results.append({"url": url, "title": title})
            except Exception as e:
                results.append({"url": url, "error": str(e)})
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print("[+] Saved onion crawl to", out)
    return out

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 darkweb_crawler.py onion_list.txt")
        sys.exit(1)
    crawl_list(sys.argv[1], out="dark_pages.json")
