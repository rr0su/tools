"""
orchestrator.py
---------------
Master runner that executes selected collectors then ingestion and alerting.
Sequential by default to be easier to control.
"""

import os, json, subprocess, argparse

def run(cmd):
    print("[*] RUN:", cmd)
    rc = os.system(cmd)
    if rc != 0:
        print("[-] Command failed:", cmd)
    return rc

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    args = parser.parse_args()
    domain = args.domain

    # 1) collect crt.sh
    run(f"python3 collectors/crtsh_collector.py {domain}")
    # 2) run pdf metadata if folder exists
    if os.path.exists("data/docs"):
        run("python3 collectors/pdf_meta.py --folder data/docs --out pdf_metadata.json")
    # 3) GitHub scan for org (assume org name == domain prefix)
    org = domain.split('.')[0]
    run(f"python3 collectors/github_monitor.py --org {org} --token $GITHUB_TOKEN --out github_findings.json")
    # 4) optional dark web crawl (requires onion list)
    if os.path.exists("onion_list.txt"):
        run("python3 collectors/darkweb_crawler.py onion_list.txt")
    # 5) ingest into Neo4j
    run("python3 ingest/neo4j_ingest.py")
    # 6) push MISP if available
    run("python3 ingest/misp_push.py")
    # 7) send Slack alert
    run("python3 slack_alert.py")
    print("[+] Pipeline finished")

if __name__ == "__main__":
    main()
