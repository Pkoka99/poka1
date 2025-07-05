#!/usr/bin/env python3
import os, time

# ── Telegram credentials ─────────────────────────────────────────────
BOT_TOKEN = "8067414697:AAGKY6wj90vn2U8ikSloAbXCkYICnmelixg"
CHAT_ID   = "5077777510"
# ─────────────────────────────────────────────────────────────────────

ARCHIVE = "tmate-2.4.0-static-linux-i386.tar.xz"
DIR     = "tmate-2.4.0-static-linux-i386"
SOCKET  = "/tmp/tmate.sock"
TXTFILE = "tmate_ssh.txt"

def sh(cmd):          # run & discard output
    os.system(cmd)

def sout(cmd):        # run & capture stdout
    return os.popen(cmd).read().strip()

# 1) your original command sequence (unchanged)
sh("pkill -9 tmate || true")
if not os.path.exists(ARCHIVE):
    sh(f"wget -nc https://github.com/tmate-io/tmate/releases/download/2.4.0/{ARCHIVE} -q")
if not os.path.isdir(DIR):
    sh(f"tar --skip-old-files -xf {ARCHIVE}")
sh(f"rm -f nohup.out; bash -ic 'nohup ./{DIR}/tmate -S {SOCKET} new-session -d & disown -a' > /dev/null 2>&1")
sh(f"./{DIR}/tmate -S {SOCKET} wait tmate-ready > /dev/null 2>&1")

# 2) fetch the SSH attach string
ssh_cmd = sout(f"./{DIR}/tmate -S {SOCKET} display -p '#{{tmate_ssh}}'").strip() + " -t"

# 3) write to a text file
with open(TXTFILE, "w") as f:
    f.write(ssh_cmd + "\n")

# 4) read it back and send to Telegram
with open(TXTFILE) as f:
    msg = f.read().strip()

os.system(
    f'curl -s -X POST "https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" '
    f'-d chat_id={CHAT_ID} --data-urlencode "text={msg}"'
)

# also echo to the local console
print(msg)
