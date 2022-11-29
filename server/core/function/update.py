import os
import requests

from utils import read_json, write_json
from constants import CONFIG_PATH


def updateData(url):

    BASE_URL_LIST = [
        ("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata", './data'),
        ("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android", './data/announce')
    ]

    for index in BASE_URL_LIST:
        if index[0] in url:
            if not os.path.isdir(index[1]):
                os.makedirs(index[1])
            localPath = url.replace(index[0], index[1])
            break

    if not os.path.isdir('./data/excel/'):
        os.makedirs('./data/excel/')

    if "Android/version" in url:
        data = read_json(CONFIG_PATH)["version"]["android"]
        return data

    try:
        data = requests.get(url).json()
        write_json(data, localPath)

    except:
        data = read_json(localPath, encoding = "utf-8")

    return data
