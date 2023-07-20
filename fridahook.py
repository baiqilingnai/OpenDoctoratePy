import sys
from base64 import b64decode

import frida

sys.path.append("server")
from server.constants import CONFIG_PATH
from server.utils import read_json

server = read_json(CONFIG_PATH)["server"]
HOST = server["host"]
PORT = server["port"]
MODE = server["mode"]

def on_message(message, data):
    print("[%s] => %s" % (message, data))

def main():
    device = frida.get_usb_device(timeout=1)

    if MODE == "cn":
        pid = device.spawn(
            b64decode('Y29tLmh5cGVyZ3J5cGguYXJrbmlnaHRz').decode())
        device.resume(pid)
        session = device.attach(pid)

    elif MODE == "global":
        pid = device.spawn(
            b64decode('Y29tLllvU3RhckVOLkFya25pZ2h0cw==').decode())
        device.resume(pid)
        session = device.attach(pid, realm="emulated")

    with open("_.js", encoding="utf-8") as f:
        s = f.read()

    s = s.replace(
        "@@@DOCTORATE@@@HOST@@@", HOST, 1
    ).replace(
        "@@@DOCTORATE@@@PORT@@@", str(PORT), 1
    )

    script = session.create_script(s)
    script.on('message', on_message)
    script.load()
    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()

if __name__ == '__main__':
    main()
