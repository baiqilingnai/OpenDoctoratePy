import os
import socket
import hashlib
from datetime import datetime

import requests
from flask import Response, stream_with_context

from constants import CONFIG_PATH
from utils import read_json

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}

def writeLog(data):
    time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    clientIp = socket.gethostbyname(socket.gethostname())
    print(f'{clientIp} - - [{time}] {data}')


def getFile(assetsHash, fileName):
    version = read_json(CONFIG_PATH)["version"]["android"]["resVersion"]
    basePath  = os.path.join('.', 'assets', version)

    if not os.path.isdir(basePath):
        os.makedirs(basePath)
    filePath = os.path.join(basePath, fileName)

    wrongSize = False
    if not os.path.basename(fileName) == 'hot_update_list.json':
        temp_hot_update_path = os.path.join(basePath, "hot_update_list.json")
        hot_update = read_json(temp_hot_update_path)
        if os.path.exists(filePath):
            for pack in hot_update["packInfos"]:
                if pack["name"] == fileName.rsplit(".", 1)[0]:
                    wrongSize = os.path.getsize(filePath) != pack["totalSize"]
                    break

    writeLog('/{}/{}'.format(version, fileName))
    return export('https://ak.hycdn.cn/assetbundle/official/Android/assets/{}/{}'.format(version, fileName), filePath, wrongSize)


def downloadFile(url, filePath):

    writeLog('\033[1;33mDownload {}\033[0;0m'.format(os.path.basename(filePath)))
    file = requests.get(url, headers=header, stream=True)

    with open(filePath, 'wb') as f:
        for chunk in file.iter_content(chunk_size=512):
            f.write(chunk)
            yield chunk


def export(url, filePath, redownload = False):

    headers = {
        "cache-control": "no-cache, no-store, must-revalidate",
        "content-disposition": "attachment; filename=" + os.path.basename(filePath),
        "content-type": "application/octet-stream",
        "expires": "0",
        "etag": hashlib.md5(filePath.encode('utf-8')).hexdigest(),
        "last-modified": datetime.now(),
        "pragma": "no-cache"
    }

    if os.path.exists(filePath) and not redownload:
        with open(filePath, "rb") as f:
            data = f.read()
        
        headers["content-length"] = os.path.getsize(filePath)
        return Response(
            data,
            headers=headers
        )

    file = requests.head(url, headers=header)
    total_size_in_bytes = int(file.headers.get('Content-length', 0))
    headers["content-length"] = total_size_in_bytes

    if os.path.basename(filePath) == 'hot_update_list.json':
        file = requests.get(url, headers=header)
        with open(filePath, 'wb') as f:
            f.write(file.content)
        
        return Response(
            file.content,
            headers=headers
        )
            
    return Response(
        stream_with_context(downloadFile(url, filePath)),
        headers=headers
    )
