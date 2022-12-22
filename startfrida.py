import os
import sys
import lzma
import time
import subprocess
from contextlib import suppress
import json

import requests
from ppadb.client import Client as AdbClient

mitmproxy_server = json.load(open('./config/config.json', 'r'))["mitmproxy"]
mitmproxy_port = mitmproxy_server["port"]

ADB_PATH = "platform-tools\\adb.exe"

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
time.sleep(5) # Sleep for 5 seconds to make sure that the emulator is rooted

print("\nRunning frida\nNow you can start fridahook\n")
os.system(f'{ADB_PATH} reverse tcp:8080 tcp:{mitmproxy_port}')
os.system(f'{ADB_PATH} shell "/data/local/tmp/frida-server" &')
