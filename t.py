import os
import time

BOT_TOKEN = "8067414697:AAGKY6wj90vn2U8ikSloAbXCkYICnmelixg"
CHAT_ID = "5077777510"
TMATE_URL = "https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-i386.tar.xz"
ARCHIVE = "tmate-2.4.0-static-linux-i386.tar.xz"
FOLDER = "tmate-2.4.0-static-linux-i386"
SOCKET = "/tmp/tmate.sock"

def run(cmd):
    return os.system(cmd)

def output(cmd):
    return os.popen(cmd).read().strip()

def main():
    # Kill old tmate
    run("pkill -9 tmate || true")

    # Download if not exists
    if not os.path.exists(ARCHIVE):
        run(f"wget {TMATE_URL}")

    # Extract only if folder doesn't exist
    if not os.path.exists(FOLDER):
        run(f"tar -xf {ARCHIVE}")

    # Start tmate session
    run(f"nohup ./{FOLDER}/tmate -S {SOCKET} new-session -d &")

    # Wait until tmate is ready
    print("⌛ Waiting for tmate...")
    run(f"./{FOLDER}/tmate -S {SOCKET} wait tmate-ready")

    # Get SSH string
    ssh_cmd = output(f"./{FOLDER}/tmate -S {SOCKET} display -p '#{{tmate_ssh}} -t'")
    print(f"✅ SSH: {ssh_cmd}")

    # Send to Telegram
    telegram_api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"tmate ready:\n`{ssh_cmd}`"
    send_cmd = f"curl -s -X POST {telegram_api} -d chat_id={CHAT_ID} -d text='{message}' -d parse_mode=Markdown"
    run(send_cmd)

if __name__ == "__main__":
    main()
