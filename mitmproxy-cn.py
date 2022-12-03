import json
import mitmproxy.http

server = json.load(open('./config/config.json', 'r'))["server"]

host = server["host"]
port = server["port"]


class AKRedirect:

    DOMAINS_LIST = [
        'android.bugly.qq.com',
        'ak-conf.hypergryph.com',
        'bi-track.hypergryph.com',
        'down.anticheatexpert.com',
        'log.trackingio.com',
        'wkdcm2.tingyun.com'
    ]

    def __init__(self):
        print('Addon for Redirecting Arknight [EN] Loaded !')

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        for domain in self.DOMAINS_LIST:
            if domain in flow.request.pretty_host:
                if domain == 'ak-conf.hypergryph.com':
                    flow.request.scheme = 'http'
                    flow.request.host = host
                    flow.request.port = port
                else:
                    flow.request.host = '0.0.0.0'

    request = http_connect

addons = [
    AKRedirect()
]