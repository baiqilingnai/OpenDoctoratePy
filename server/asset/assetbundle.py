import os
import socket
import hashlib
import requests

from datetime import datetime
from flask import make_response
from utils import read_json, write_json


def writeLog(data):
    time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    clientIp = socket.gethostbyname(socket.gethostname())
    print(f'{clientIp} - - [{time}] {data}')


def getFile(assetsHash, fileName):
    version = read_json('./config/config.json')["version"]["android"]["resVersion"]
        
    basePath  = './assets/' + version + '/'

    if not os.path.isdir(basePath):
        os.makedirs(basePath)

    filePath = basePath + fileName

    if os.path.exists(filePath):
        return export(filePath, assetsHash)

    writeLog('\033[1;33mDownload {}\033[0;0m'.format(fileName))

    downloadFile('https://ak.hycdn.cn/assetbundle/official/Android/assets/{}/{}'.format(version, fileName), filePath)

    if os.path.exists(filePath):
        writeLog('/{}/{}'.format(version, fileName))
        return export(filePath, assetsHash)
    
    return None


def downloadFile(url, filePath):

    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}

    file = requests.get(url, headers=header, timeout=3.0, stream=False) # Solve 'High Concurrency'

    with open(filePath, 'wb') as f:
        for chunk in file.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)

    return None


def export(file, assetsHash):
    
    if file == None:
        return None

    with open(file, 'rb') as f:
        data = f.read()

    response = make_response(data)
    response.headers["cache-control"] = "no-cache, no-store, must-revalidate"
    response.headers["content-disposition"] = "attachment; filename=" + os.path.basename(file)
    response.headers["content-length"] = os.path.getsize(file)
    response.headers["content-type"] = "application/octet-stream"
    response.headers["expires"] = "0"
    response.headers["etag"] = hashlib.md5(file.encode('utf-8')).hexdigest()
    response.headers["last-modified"] = datetime.now()
    response.headers["pragma"] = "no-cache"

    if os.path.basename(file) == 'hot_update_list.json':
        if os.path.exists(file):
            hot_update_list = read_json(file)
        else:
            hot_update_list = requests.get('https://ak.hycdn.cn/assetbundle/official/Android/assets/{}/hot_update_list.json'.format(assetsHash)).json()
            
        abInfoList = hot_update_list["abInfos"]
        newAbInfos = []
        ######## TODO: Add mods ########
        modsList = []
        
        for abInfo in abInfoList:
            if abInfo["name"] not in modsList:
                newAbInfos.append(abInfo)
        i = 0
        while i < len(modsList):
            newAbInfos.append(modsList[i])
            i += 1
        ######## TODO: Add mods ########

        hot_update_list["abInfos"] = newAbInfos
        write_json(hot_update_list, file)

    return response