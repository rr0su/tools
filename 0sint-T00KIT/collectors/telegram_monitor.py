"""
telegram_monitor.py
-------------------
Scrape public Telegram channels using Telethon (API-based).
Uses a burner account and stores messages that match keywords.
"""

from telethon import TelegramClient, events, sync
import asyncio, json, argparse, os

def run_monitor(api_id, api_hash, channels, keywords, out="tg_messages.json"):
    client = TelegramClient('tg_session', api_id, api_hash)
    collected = []

    async def main():
        await client.start()
        for ch in channels:
            entity = await client.get_entity(ch)
            async for message in client.iter_messages(entity, limit=200):
                text = message.message or ""
                if any(k.lower() in text.lower() for k in keywords):
                    collected.append({
                        "channel": ch, "id": message.id, "text": text, "date": str(message.date)
                    })
        await client.disconnect()
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(collected, fh, indent=2)
        print("[+] Saved Telegram matches to", out)

    client.loop.run_until_complete(main())

if __name__ == "__main__":
    import sys
    api_id = int(os.getenv("TG_API_ID", 0))
    api_hash = os.getenv("TG_API_HASH", "")
    if not api_id or not api_hash:
        print("Set TG_API_ID and TG_API_HASH environment variables.")
        sys.exit(1)
    channels = ["some_public_channel"]
    keywords = ["leak", "target.com", "password"]
    run_monitor(api_id, api_hash, channels, keywords)
