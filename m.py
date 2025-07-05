#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import requests   # pip install requests

TOKEN   = "8067414697:AAGKY6wj90vn2U8ikSloAbXCkYICnmelixg"   # ← token botmu
CHAT_ID = "5077777510"                                        # ← id chat / group

# 1. Buka file & ambil link
link_file = pathlib.Path("tmate.txt")
link      = link_file.read_text().strip()            # hapus \n di ujung

# 2. Susun pesan
message = f"{link}"

# 3. Kirim ke Telegram
url  = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
resp = requests.post(url, data={"chat_id": CHAT_ID, "text": message})

# 4. Cek hasil (optional)
print("Status:", resp.status_code)
print("Response:", resp.json())
