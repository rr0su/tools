"""
misp_push.py
------------
Push selected high-confidence indicators to MISP.
"""

import json, os
from pymisp import ExpandedPyMISP

conf = json.load(open("config.json"))
misp = ExpandedPyMISP(conf["MISP"]["url"], conf["MISP"]["key"], ssl=conf["MISP"].get("ssl", False))

def push_simple_event(domain, emails, note="OSINT feed"):
    event = misp.new_event(info=f"OSINT: {domain}", distribution=0, threat_level_id=2, analysis=0)
    for e in emails:
        misp.add_named_attribute(event, 'email-src', e)
    misp.add_named_attribute(event, 'domain', domain)
    print("[+] Pushed event:", event['Event']['id'])

if __name__ == "__main__":
    j = json.load(open("intel.json"))
    push_simple_event(j["domain"], j["emails"])
