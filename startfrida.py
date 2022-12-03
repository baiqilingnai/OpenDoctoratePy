import os
import sys
import lzma
import time
import subprocess
from contextlib import suppress

import requests
from ppadb.client import Client as AdbClient

ADB_PATH = "platform-tools\\adb.exe"

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

frida_exists = device.shell('test -f /data/local/tmp/frida-server && echo True').strip()
with suppress(RuntimeError):
    device.root()

if not frida_exists:
    architecture = device.shell("getprop ro.product.cpu.abi").strip().replace("-v8a", "")
    print(f"Architexture: {architecture}")

    version = requests.get("https://api.github.com/repos/frida/frida/releases/latest").json()["tag_name"]
    name = f"frida-server-{version}-android-{architecture}"
    print(f"Download {name}...")
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


print("\nRunning frida\nNow you can start fridahook")
device.shell("/data/local/tmp/frida-server")
print("If you see this then frida-server didn't run properly. Try running it again.")
input("Press enter to continue: ")