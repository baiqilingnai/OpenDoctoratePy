import json
import base64

from constants import CONFIG_PATH
from utils import read_json

ASSETBUNDLE = read_json(CONFIG_PATH)["assetbundle"]["enable"]


def prodAndroidVersion():

    version = read_json(CONFIG_PATH)["assetbundle"]["version"]["android"]

    return version


def prodNetworkConfig():

    FUNC_VER = "V033"
    HU = "https://ak.hycdn.cn"
    HV = "https://ak-conf.hypergryph.com"

    if ASSETBUNDLE:
        HU = read_json(CONFIG_PATH)["assetbundle"]["server"]["url"]
        HV = "http://127.0.0.1:8443"

    network_config = json.dumps({
        "sign": "sign",
        "content": json.dumps({
            "configVer": "5",
            "funcVer": FUNC_VER,
            "configs": {FUNC_VER: {"override": True, "network": json.loads(base64.b64decode("eyJncyI6ICJodHRwOi8vMTI3LjAuMC4xOjg0NDMiLCAiYXMiOiAiaHR0cDovLzEyNy4wLjAuMTo4NDQzIiwgInU4IjogImh0dHA6Ly8xMjcuMC4wLjE6ODQ0My91OCIsICJodSI6ICJ7SFV9L2Fzc2V0YnVuZGxlL29mZmljaWFsIiwgImh2IjogIntIVn0vY29uZmlnL3Byb2Qvb2ZmaWNpYWwvezB9L3ZlcnNpb24iLCAicmMiOiAiaHR0cDovLzEyNy4wLjAuMTo4NDQzL2NvbmZpZy9wcm9kL29mZmljaWFsL3JlbW90ZV9jb25maWciLCAiYW4iOiAiaHR0cHM6Ly9hay1jb25mLmh5cGVyZ3J5cGguY29tL2NvbmZpZy9wcm9kL2Fubm91bmNlX21ldGEvezB9L2Fubm91bmNlbWVudC5tZXRhLmpzb24iLCAicHJlYW4iOiAiaHR0cHM6Ly9hay1jb25mLmh5cGVyZ3J5cGguY29tL2NvbmZpZy9wcm9kL2Fubm91bmNlX21ldGEvezB9L3ByZWFubm91bmNlbWVudC5tZXRhLmpzb24iLCAic2wiOiAiaHR0cHM6Ly9hay5oeXBlcmdyeXBoLmNvbS9wcm90b2NvbC9zZXJ2aWNlIiwgIm9mIjogImh0dHBzOi8vYWsuaHlwZXJncnlwaC5jb20vaW5kZXguaHRtbCIsICJwa2dBZCI6IG51bGwsICJwa2dJT1MiOiBudWxsLCAic2VjdXJlIjogZmFsc2V9").decode().replace("{HU}", HU).replace("{HV}", HV))}}
        })
    })

    return network_config


def prodRemoteConfig():

    remote = json.dumps({})

    return remote


def prodPreAnnouncement():

    return read_json('./data/announce/preannouncement.meta.json', encoding='utf-8')


def prodAnnouncement():

    return read_json('./data/announce/announcement.meta.json', encoding='utf-8')