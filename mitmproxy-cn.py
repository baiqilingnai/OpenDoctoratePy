import json
import base64
import mitmproxy.http

FUNC_VER = "V033"

network_config = json.dumps({
    "sign": "sign",
    "content": json.dumps({
        "configVer": "5",
        "funcVer": FUNC_VER,
        "configs": {FUNC_VER: {"override": True, "network": json.loads(base64.b64decode("eyJncyI6ICJodHRwOi8vMTI3LjAuMC4xOjg0NDMiLCAiYXMiOiAiaHR0cDovLzEyNy4wLjAuMTo4NDQzIiwgInU4IjogImh0dHA6Ly8xMjcuMC4wLjE6ODQ0My91OCIsICJodSI6ICJodHRwczovL2FrLmh5Y2RuLmNuL2Fzc2V0YnVuZGxlL29mZmljaWFsIiwgImh2IjogImh0dHBzOi8vYWstY29uZi5oeXBlcmdyeXBoLmNvbS9jb25maWcvcHJvZC9vZmZpY2lhbC97MH0vdmVyc2lvbiIsICJyYyI6ICJodHRwczovL2FrLWNvbmYuaHlwZXJncnlwaC5jb20vY29uZmlnL3Byb2Qvb2ZmaWNpYWwvcmVtb3RlX2NvbmZpZyIsICJhbiI6ICJodHRwczovL2FrLWNvbmYuaHlwZXJncnlwaC5jb20vY29uZmlnL3Byb2QvYW5ub3VuY2VfbWV0YS97MH0vYW5ub3VuY2VtZW50Lm1ldGEuanNvbiIsICJwcmVhbiI6ICJodHRwczovL2FrLWNvbmYuaHlwZXJncnlwaC5jb20vY29uZmlnL3Byb2QvYW5ub3VuY2VfbWV0YS97MH0vcHJlYW5ub3VuY2VtZW50Lm1ldGEuanNvbiIsICJzbCI6ICJodHRwczovL2FrLmh5cGVyZ3J5cGguY29tL3Byb3RvY29sL3NlcnZpY2UiLCAib2YiOiAiaHR0cHM6Ly9hay5oeXBlcmdyeXBoLmNvbS9pbmRleC5odG1sIiwgInBrZ0FkIjogbnVsbCwgInBrZ0lPUyI6IG51bGwsICJzZWN1cmUiOiBmYWxzZX0=").decode())}}
    })
})

class AKRedirect:

    def __init__(self):
        print('Addon for Redirecting Arknight [EN] Loaded !')

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if 'bi-track.hypergryph.com' in flow.request.pretty_host:
            flow.request.scheme = 'http'
            flow.request.host = "localhost"

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if 'network_config' in flow.request.pretty_url:
            flow.response.set_text(network_config)
        
        if 'remote_config' in flow.request.pretty_url:
            flow.response.set_text(json.dumps({}))

addons = [
    AKRedirect()
]
