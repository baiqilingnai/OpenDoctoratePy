import os
import sys
import time
import shutil
import subprocess
from contextlib import suppress

from ppadb.client import Client as AdbClient

cert_file_path = os.path.join(os.environ['USERPROFILE'], ".mitmproxy", "mitmproxy-ca-cert.cer")
if not os.path.exists(cert_file_path):
    print("Launching mitmproxy for first time")
    p = subprocess.Popen("mitmdump")
    time.sleep(5)
    p.kill()

print("Connecting to currently opened emulator")
client = AdbClient(host="127.0.0.1", port=5037)
p = subprocess.Popen("adb start-server")
count = 0
while True:
    try:
        devices = client.devices()
        break
    except RuntimeError:
        count += 1
        if count == 5:
            print("Cannot connect to emulator. Check adb connection and retry.")
            sys.exit(0)
        pass
if len(devices) > 1:
    print("Multiple adb connections detected. Select one to connect to.")
    for d in devices:
        print(f"{devices.index(d) + 1}. {d.serial}")
    index = int(input("Input Number: "))
    device = devices[index-1]
elif len(devices) < 1:
    print("No adb devices detected. Try typing <adb devices> in cmd a couple of times and try again.")
    input("Press enter to continue: ")
    sys.exit(0)
else:
    device = devices[0]

cert_exists = device.shell('test -f /storage/emulated/0/Pictures/mitmproxy-ca-cert.cer && echo True').strip()
if cert_exists:
    print("Mitmproxy cert is already installed as system certificate. Exiting....")
    sys.exit(0)

with suppress(RuntimeError):
    device.root()

shutil.copy(cert_file_path, os.path.join(os.getcwd(), "mitmproxy-ca-cert.cer"))
print("Copying mitmproxy certificate...")
try:
    device.push("mitmproxy-ca-cert.cer", "/storage/emulated/0/Pictures/mitmproxy-ca-cert.cer")
except RuntimeError as e:
    print(e)
    sys.exit(0)

print("Mitmproxy certificate is installed!")
os.remove("mitmproxy-ca-cert.cer")
input("Press enter to exit...")