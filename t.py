#!/usr/bin/env python3
import subprocess, os, time, urllib.parse, urllib.request, shutil, sys, textwrap

# ───--- USER SETTINGS ---───
BOT_TOKEN = "8067414697:AAGKY6wj90vn2U8ikSloAbXCkYICnmelixg"
CHAT_ID   = "5077777510"
TMATE_URL = "https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-i386.tar.xz"
ARCHIVE   = TMATE_URL.split("/")[-1]
EXTRACTED = "tmate-2.4.0-static-linux-i386"
SOCKET    = "/tmp/tmate.sock"
# ──────────────────────────

def run(cmd, check=True, **kwargs):
    """Thin wrapper around subprocess.run that prints the command first."""
    print(f"+ {cmd}")
    return subprocess.run(cmd, shell=True, check=check, **kwargs)

def ensure_tmate():
    """Download & extract tmate if it isn't already present."""
    if not shutil.which(f"./{EXTRACTED}/tmate"):
        # 1) Kill any old tmate
        run("pkill -9 tmate || true", check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 2) Download archive (skip if already exists)
        if not os.path.exists(ARCHIVE):
            run(f"wget -nc {TMATE_URL}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 3) Extract while keeping existing files intact
        run(f"tar --skip-old-files -xf {ARCHIVE}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_tmate():
    """Start a detached tmate session bound to a specific socket."""
    cmd = f"nohup ./{EXTRACTED}/tmate -S {SOCKET} new-session -d & disown"
    run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def wait_ready():
    """Block until tmate signals readiness."""
    cmd = f"./{EXTRACTED}/tmate -S {SOCKET} wait tmate-ready"
    run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def fetch_ssh_string() -> str:
    """Return the public SSH string announced by tmate."""
    cmd = f"./{EXTRACTED}/tmate -S {SOCKET} display -p '#{{tmate_ssh}} -t'"
    proc = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
    return proc.stdout.strip()

def send_to_telegram(message: str):
    """Fire-and-forget HTTP request to Telegram Bot API."""
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": message}).encode()
    with urllib.request.urlopen(api_url, data=data, timeout=10) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Telegram API responded with HTTP {resp.status}")

def main():
    ensure_tmate()
    start_tmate()
    wait_ready()
    ssh = fetch_ssh_string()

    banner = textwrap.dedent(f"""\
        ✅ *tmate tunnel is ready!*
        ```
        {ssh}
        ```
        _Copy & paste the command above to attach to this session_
    """)
    print(banner)

    try:
        send_to_telegram(banner)
        print("🔔 Sent to Telegram successfully.")
    except Exception as e:
        print(f"❌ Failed to notify Telegram: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
