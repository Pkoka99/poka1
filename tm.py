#!/usr/bin/env python3
import subprocess, os, platform, urllib.parse, urllib.request, shutil, sys, textwrap, re

BOT_TOKEN = "8067414697:AAGKY6wj90vn2U8ikSloAbXCkYICnmelixg"
CHAT_ID   = "5077777510"

VERSION   = "2.4.0"
ARCH_MAP  = {
    "x86_64":  "x86_64",
    "amd64":   "x86_64",
    "i386":    "i386",
    "i686":    "i386",
    "aarch64": "arm64v8",
    "arm64":   "arm64v8",
    "armv7l":  "armhf",
}
arch = ARCH_MAP.get(platform.machine())
if not arch:
    sys.exit(f"❌ Unsupported arch: {platform.machine()}")

ARCHIVE   = f"tmate-{VERSION}-static-linux-{arch}.tar.xz"
TMATE_URL = f"https://github.com/tmate-io/tmate/releases/download/{VERSION}/{ARCHIVE}"
EXTRACTED = re.sub(r"\.tar\.xz$", "", ARCHIVE)
SOCKET    = "/tmp/tmate.sock"

def run(cmd, **kw):
    kw.setdefault("shell", True)
    kw.setdefault("check", True)
    return subprocess.run(cmd, **kw)

def ensure_tmate():
    if not shutil.which(f"./{EXTRACTED}/tmate"):
        run("pkill -9 tmate || true", check=False, stdout=subprocess.DEVNULL)
        if not os.path.exists(ARCHIVE):
            run(f"wget -nc {TMATE_URL}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        run(f"tar --skip-old-files -xf {ARCHIVE}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        run(f"chmod +x ./{EXTRACTED}/tmate")

def start_tmate():
    run(f"nohup ./{EXTRACTED}/tmate -S {SOCKET} new-session -d & disown",
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def wait_ready():
    run(f"./{EXTRACTED}/tmate -S {SOCKET} wait tmate-ready",
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_ssh():
    out = run(f"./{EXTRACTED}/tmate -S {SOCKET} display -p '#{{tmate_ssh}} -t'",
              text=True, capture_output=True)
    return out.stdout.strip()

def telegram(msg):
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode()
    with urllib.request.urlopen(url, data, timeout=10) as r:
        if r.status != 200:
            raise RuntimeError(f"Telegram HTTP {r.status}")

def main():
    ensure_tmate()
    start_tmate()
    wait_ready()
    ssh = get_ssh()
    banner = textwrap.dedent(f"""\
        ✅ *tmate ready*
        ```
        {ssh}
        ```
        _Copy-paste to attach_
    """)
    print(banner)
    telegram(banner)

if __name__ == "__main__":
    main()
