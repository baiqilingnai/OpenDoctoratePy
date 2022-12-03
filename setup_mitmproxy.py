import os
import sys
import time
import shutil
import subprocess
from zipfile import ZipFile
from contextlib import suppress

import requests
from ppadb.client import Client as AdbClient

CERT_FILE_PATH = os.path.join(os.environ['USERPROFILE'], ".mitmproxy", "mitmproxy-ca-cert.cer")
ADB_PATH = "platform-tools\\adb.exe"

if not os.path.exists(CERT_FILE_PATH):
    print("Launching mitmproxy for first time")
    p = subprocess.Popen("mitmdump")
    time.sleep(5)
    p.kill()


if not os.path.exists(ADB_PATH):
    print("No adb file found. Downloading the latest version.")
    r = requests.get("https://dl.google.com/android/repository/platform-tools-latest-windows.zip", allow_redirects=True)
    open('adb.zip', 'wb').write(r.content)
    ZipFile('adb.zip').extractall(".")
    os.remove('adb.zip')


while True:
    os.system('cls')
    print("Restarting server")
    subprocess.run(f"{ADB_PATH} kill-server")
    subprocess.run(f"{ADB_PATH} start-server")
    time.sleep(5)

    print("Connecting to currently opened emulator")
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if len(devices) < 1:
        print("No adb devices detected. Make sure that an emulator is running and has adb connection open.")
        input("Enter to retry..")
        sys.exit(0)
    elif len(devices) > 1:
        continue
    else:
        device = devices[0]
        break

cert_exists = device.shell('test -f /storage/emulated/0/Pictures/mitmproxy-ca-cert.cer && echo True').strip()
if cert_exists:
    print("Mitmproxy cert is already installed as system certificate. Exiting....")
    sys.exit(0)

with suppress(RuntimeError):
    device.root()

shutil.copy(CERT_FILE_PATH, os.path.join(os.getcwd(), "mitmproxy-ca-cert.cer"))
print("Copying mitmproxy certificate...")
try:
    device.push("mitmproxy-ca-cert.cer", "/storage/emulated/0/Pictures/mitmproxy-ca-cert.cer")
except RuntimeError as e:
    print(e)
    sys.exit(0)

print("Mitmproxy certificate is installed!")
os.remove("mitmproxy-ca-cert.cer")
input("Press enter to exit...")