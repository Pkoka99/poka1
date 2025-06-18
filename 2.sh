rm -r vv.py
rm -r google-chrome-stable_current_amd64.deb
rm -r chromedriver-linux64
rm -r chromedriver-linux64.zip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
wget https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.103/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver
mv chromedriver-linux64/chromedriver /usr/local/bin/
pip install selenium --break-system-packages --ignore-installed && pip install --upgrade pip
wget https://raw.githubusercontent.com/Pkoka99/Pkoka99/refs/heads/main/vv.py
python vv.py
