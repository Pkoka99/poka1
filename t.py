import os

# ─── Telegram credentials ───
BOT_TOKEN = "8067414697:AAGKY6wj90vn2U8ikSloAbXCkYICnmelixg"
CHAT_ID   = "5077777510"
# ────────────────────────────

# 1. Run your exact shell sequence
os.system("pkill -9 tmate")
os.system("wget -nc https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-i386.tar.xz -q")
os.system("tar --skip-old-files -xf tmate-2.4.0-static-linux-i386.tar.xz")
os.system("rm -f nohup.out; bash -ic 'nohup ./tmate-2.4.0-static-linux-i386/tmate -S /tmp/tmate.sock new-session -d & disown -a' > /dev/null 2>&1")
os.system("./tmate-2.4.0-static-linux-i386/tmate -S /tmp/tmate.sock wait tmate-ready > /dev/null 2>&1")

# 2. Grab the SSH attach string
ssh_cmd = os.popen("./tmate-2.4.0-static-linux-i386/tmate -S /tmp/tmate.sock display -p '#{tmate_ssh} -t'").read().strip()

# 3. Send it to Telegram (curl invoked via os.system)
os.system(
    f'curl -s -X POST https://api.telegram.org/bot{BOT_TOKEN}/sendMessage '
    f'-d chat_id={CHAT_ID} --data-urlencode "text={ssh_cmd}" > /dev/null'
)

# 4. Echo locally as well
print(ssh_cmd)
