osint-apex-toolkit/
├─ config.example.json
├─ README.md
├─ requirements.txt
├─ orchestrator.py
├─ collectors/
│  ├─ __init__.py
│  ├─ pdf_meta.py
│  ├─ github_monitor.py
│  ├─ shodan_monitor.py
│  ├─ telegram_monitor.py
│  ├─ crtsh_collector.py
│  └─ darkweb_crawler.py
├─ ingest/
│  ├─ neo4j_ingest.py
│  └─ misp_push.py
├─ webhook/
│  └─ webhook_api.py
├─ utils/
│  ├─ storage.py
│  ├─ opsec.py
│  └─ alerts.py
└─ examples/
   └─ sample_intel.json
