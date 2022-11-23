import json
import base64
import mitmproxy.http


class AKRedirect:

    def __init__(self):
        print('Addon for Redirecting Arknight [EN] Loaded !')

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        if 'ak-conf.hypergryph.com' in flow.request.pretty_host:
            flow.request.scheme = 'http'
            flow.request.host = "127.0.0.1"
            flow.request.port = 8443

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if 'bi-track.hypergryph.com' in flow.request.pretty_host:
            flow.request.scheme = 'http'
            flow.request.host = "127.0.0.1"

        if 'ak-conf.hypergryph.com' in flow.request.pretty_host:
            flow.request.scheme = 'http'
            flow.request.host = "127.0.0.1"
            flow.request.port = 8443

addons = [
    AKRedirect()
]
