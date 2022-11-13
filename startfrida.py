import os
import sys
import lzma
from contextlib import suppress

import requests
from ppadb.client import Client as AdbClient

print("Connecting to currently opened emulator")
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
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

frida_exists = device.shell('test -f /data/local/tmp/frida-server && echo True').strip()
with suppress(RuntimeError):
    device.root()

if not frida_exists:
    architecture = device.shell("getprop ro.product.cpu.abi").strip()
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