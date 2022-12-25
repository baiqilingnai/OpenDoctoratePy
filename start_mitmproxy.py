import json
import os

mitmproxy_server = json.load(open('./config/config.json', 'r'))["mitmproxy"]

mitmproxy_port = mitmproxy_server["port"]

os.system(
    f"mitmdump.exe --set connection_strategy=lazy --listen-host 127.0.0.1 --listen-port {mitmproxy_port} -s mitmproxy-cn.py"
)
