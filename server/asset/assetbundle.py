import os
import json
import socket
import requests
import hashlib

from flask import Flask, make_response
from datetime import datetime
from gevent import pywsgi
 
app = Flask(__name__)
os.system("")


@app.route('/assetbundle/official/Android/assets/<string:assetsHash>/<string:fileName>', methods=["GET"])
def getFile(assetsHash, fileName):

    with open('./config/config.json') as f:
        version = json.load(f)["assetbundle"]["version"]["android"]["resVersion"]
        
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clientIp = socket.gethostbyname(socket.gethostname())
    filePath  = './assets/' + version + '/'

    if not os.path.isdir(filePath):
        os.makedirs(filePath)

    newFile = filePath + fileName

    if os.path.exists(newFile):
        return exportFile(newFile, assetsHash)


    print('\033[1;33m{} - - [{}] Download {}\033[0;0m'.format(clientIp, time, fileName))
    downloadFile('https://ak.hycdn.cn/assetbundle/official/Android/assets/{}/{}'.format(version, fileName), newFile)

    if os.path.exists(newFile):
        print('{} - - [{}] /{}/{}'.format(clientIp, time, version, fileName))
        return exportFile(newFile, assetsHash)
    
    return None


def downloadFile(url, filePath):

    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}

    file = requests.get(url, headers=header, timeout=3.0, stream=True)

    with open(filePath, 'wb') as f:
        for chunk in file.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)

    return None


def exportFile(file, assetsHash):
    
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
    response.headers["last-modified"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %X GMT")
    response.headers["pragma"] = "no-cache"

    if os.path.basename(file) == 'hot_update_list.json':
        if os.path.exists(file):
            with open(file, 'r') as f:
                hot_update_list = json.load(f)
        else:
            hot_update_list = requests.get('https://ak.hycdn.cn/assetbundle/official/Android/assets/{}/hot_update_list.json'.format(assetsHash)).json()
            
        abInfoList = hot_update_list["abInfos"]
        newAbInfos = []
        ######## TODO: Add mods ########
        for abInfo in abInfoList:
            newAbInfos.append(abInfo)
        ######## TODO: Add mods ########
        hot_update_list["abInfos"] = newAbInfos
        with open(file, 'w') as f:
            json.dump(hot_update_list,f)

    return response
 

if __name__ == "__main__":
    print('Local AssetBundle Server')
    server = pywsgi.WSGIServer(('0.0.0.0', 38660), app)
    server.serve_forever()
 