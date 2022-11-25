import json
import base64
import mitmproxy.http

host = json.load(open('./config/config.json', 'r'))["server"]["host"]


class AKRedirect:

    def __init__(self):
        print('Addon for Redirecting Arknight [EN] Loaded !')

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        if 'bi-track.hypergryph.com' in flow.request.pretty_host:
            flow.request.host = '0.0.0.0'

        if 'ak-conf.hypergryph.com' in flow.request.pretty_host:
            flow.request.host = host

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if 'ak-conf.hypergryph.com' in flow.request.pretty_host:
            flow.request.scheme = 'http'
            flow.request.host = host
            flow.request.port = 8443

addons = [
    AKRedirect()
]
