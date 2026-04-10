"""
alerts.py
---------
Small helper to normalize alerts to Slack/Discord/email.
"""

import requests, os, json

def slack(text):
    webhook = os.getenv("SLACK_WEBHOOK")
    if not webhook:
        print("[!] Slack webhook not set")
        return
    requests.post(webhook, json={"text": text})

def discord(webhook, text):
    requests.post(webhook, json={"content": text})
