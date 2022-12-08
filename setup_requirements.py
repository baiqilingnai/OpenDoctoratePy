import os
import sys
import lzma
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

os.system('cls')
subprocess.run(f"{ADB_PATH} kill-server")
subprocess.run(f"{ADB_PATH} start-server")
time.sleep(3)
client = AdbClient(host="127.0.0.1", port=5037)
device = None

while True:
    num = input("Choose your emulator.\n1. Mumu Player\n2. LDPlayer9\n3. Auto\nChoose one: ")
    try:
        num = int(num)
    except:
        print("Invalid input")
        continue

    if num not in [1, 2, 3]:
        print("Invalid input")
        continue

    if num == 1:
        # Mumu Player
        print("Trying to connect to currently opened Mumu Player")
        client.remote_connect("127.0.0.1", 7555) # Default port for mumu player
        devices = client.devices()
        if len(devices) != 1:
            print("Something went wrong. Make sure that an emulator is running and has adb connection open.")
            sys.exit(0)
        device = devices[0]
        break

    elif num == 2:
        # LDPlayer9
        print("Trying to connect to currently opened LDPlayer9 Player")
        devices = client.devices() # LDPlayer9 usually auto connects to adb
        if len(devices) != 1: # If not found, try to connect manually to default port
            client.remote_connect("127.0.0.1", 5555)
            devices = client.devices()
            if len(devices) != 1:
                print("Something went wrong. Make sure that an emulator is running and has adb connection open.")
                sys.exit(0)
        device = devices[0]
        break

    elif num == 3:
        # Auto
        print("Finding an open emulator within the default port range...")
        for i in range(5554, 5682):
            print("Trying port", i, end="\r")
            client.remote_connect("127.0.0.1", i) # Default port for mumu player
            devices = client.devices()
            if len(devices) == 1:
                device = devices[0]
                print("Found emulator on port", i)
                break
        if not device:
            print("No emulator found on default port range (5554-5682). Make sure that an emulator is running and has adb connection open.")
            sys.exit(0)
        break

print("Check the emulator and accept if it asks for root permission.")
with suppress(RuntimeError):
    device.root()
time.sleep(3) # Sleep for 3 seconds to make sure that the emulator is rooted

cert_exists = device.shell('test -f /data/local/tmp/mitmproxy-ca-cert.cer && echo True').strip()
if not cert_exists:
    shutil.copy(CERT_FILE_PATH, os.path.join(os.getcwd(), "mitmproxy-ca-cert.cer"))
    print("Copying mitmproxy certificate...")
    device.push("mitmproxy-ca-cert.cer", "/data/local/tmp/mitmproxy-ca-cert.cer")

    print("Modifying permissions")
    device.shell("chmod 755 /data/local/tmp/mitmproxy-ca-cert.cer")

    print("Mitmproxy certificate is installed!")
    os.remove("mitmproxy-ca-cert.cer")


frida_exists = device.shell('test -f /data/local/tmp/frida-server && echo True').strip()
if not frida_exists:
    architecture = device.shell("getprop ro.product.cpu.abi").strip().replace("-v8a", "")
    print(f"\nArchitecture: {architecture}")

    version = requests.get("https://api.github.com/repos/frida/frida/releases/latest").json()["tag_name"]
    name = f"frida-server-{version}-android-{architecture}"
    print(f"Downloading {name}...")
    url = f"https://github.com/frida/frida/releases/download/{version}/{name}.xz"
    r = requests.get(url, allow_redirects=True)
    open('frida-server.xz', 'wb').write(r.content)

    print("Extracting....")
    with lzma.open("frida-server.xz") as f, open('frida-server', 'wb') as fout:
        file_content = f.read()
        fout.write(file_content)

    print("Copying frida-server...")
    device.push("frida-server", "/data/local/tmp/frida-server")

    print("Modifying permissions")
    device.shell("chmod 755 /data/local/tmp/frida-server")
    os.remove("frida-server")
    os.remove("frida-server.xz")

print("\nMitmproxy certificate and frida-server are installed!")
input("Press enter to exit...")