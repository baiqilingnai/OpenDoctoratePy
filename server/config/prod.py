import re
import json

from constants import CONFIG_PATH
from utils import read_json, write_json
from core.function.update import updateData


def prodAndroidVersion():

    version = read_json(CONFIG_PATH)["version"]["android"]

    return version


def prodNetworkConfig():

    server_config = read_json(CONFIG_PATH)

    server = "http://" + server_config["server"]["host"] + ":" + str(server_config["server"]["port"])
    network_config = server_config["networkConfig"]
    funcVer = network_config["content"]["funcVer"]

    if server_config["assets"]["autoUpdate"]:
        version = updateData("https://ak-conf.hypergryph.com/config/prod/official/Android/version")
        server_config["version"]["android"] = version

        write_json(server_config, CONFIG_PATH)

    for index in network_config["content"]["configs"][funcVer]["network"]:
        if index == "sl":
            break
        url = network_config["content"]["configs"][funcVer]["network"][index]
        
        if server_config["assets"]["enableRedirect"] == False and index in ["hu", "hv"]:
            if index == "hu":
                url = re.sub("{server}", "https://ak.hycdn.cn", url)
            url = re.sub("{server}", "https://ak-conf.hypergryph.com", url)
            network_config["content"]["configs"][funcVer]["network"][index] = url
            continue

        network_config["content"]["configs"][funcVer]["network"][index] = re.sub("{server}", server, url)

    network_config["content"] = json.dumps(network_config["content"])

    return json.dumps(network_config)


def prodRemoteConfig():

    remote = read_json(CONFIG_PATH)["remote"]

    return json.dumps(remote)


def prodPreAnnouncement():

    data = updateData("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android/preannouncement.meta.json")

    return data


def prodAnnouncement():

    data = updateData("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android/announcement.meta.json")

    return data