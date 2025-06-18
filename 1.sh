apt update && apt upgrade -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt --fix-broken install -y
dpkg -i google-chrome-stable_current_amd64.deb
wget https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.103/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver
mv chromedriver-linux64/chromedriver /usr/local/bin/
apt install python3-pip -y
python3 -m pip install selenium
wget https://raw.githubusercontent.com/Pkoka99/Pkoka99/refs/heads/main/vv.py
python3 vv.py
