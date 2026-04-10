"""
opsec.py
--------
Utility functions for OPSEC checks and safety gating.
Use these before executing any action that could be noisy.
"""

import os, subprocess

def check_tor_running(sock="127.0.0.1:9050"):
    # Very simple check
    try:
        # netstat would be used in hardened env; here we attempt to open a socket
        import socket
        s = socket.socket()
        host, port = sock.split(':')
        s.connect((host, int(port)))
        s.close()
        return True
    except Exception:
        return False

def require_env_ok():
    if os.getenv("ENV") != "lab" and not check_tor_running():
        raise SystemExit("OPSEC: Tor not running and not in lab environment. Aborting.")
