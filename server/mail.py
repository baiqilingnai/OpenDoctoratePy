from time import time

from flask import request

from constants import MAILLIST_PATH
from utils import read_json

receiveID = []
removeID = []
hasGift = 1


def mailGetMetaInfoList():

    data = request.data

    result = []
    mail_list = read_json(MAILLIST_PATH, encoding="utf-8")["mailList"]
    
    for mailId in mail_list:
        config = {
            "createAt": round(time()),
            "hasItem": 1,
            "mailId": mailId,
            "state": 0,
            "type": 1
        }
        if mailId in receiveID:
            config["state"] = 1
        if int(mailId) in removeID:
            continue
        result.append(config)

    data = {
        "result": result,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def mailListMailBox():

    data = request.data
    mails = []
    mail_list = read_json(MAILLIST_PATH, encoding="utf-8")["mailList"]

    for mailId in mail_list:
        config = {
            "createAt": round(time()),
            "expireAt": round(time()) + 31536000,
            "mailId": mailId,
            "platform": -1,
            "state": 0,
            "style": {},
            "type": 1,
            "uid": ""
        }
        if mailId in receiveID:
            config["state"] = 1

        mails.append(dict(mail_list[mailId], **config))

    data = {
        "mailList": mails,
        "playerDataDelta": {
            "modified": {
                "pushFlags": {
                    "hasGifts": hasGift
                }
            },
            "deleted": {}
        }
    }

    return data


def getItems(request_data, key):

    global receiveID, hasGift

    items = []
    mail_list = read_json(MAILLIST_PATH, encoding="utf-8")["mailList"]

    for mailId in mail_list:
        if mailId in receiveID:
            continue
        if key == "sysMailIdList":
            if "items" in mail_list[mailId] and int(mailId) in request_data[key]:
                for value in mail_list[mailId]["items"]:
                    items.append(value)
            receiveID.append(mailId)
        else:
            if "items" in mail_list[mailId] and int(mailId) == request_data[key]:
                for value in mail_list[mailId]["items"]:
                    items.append(value)
            receiveID.append(mailId)
            break

    if len(receiveID) == len(mail_list) or len(receiveID) == 0:
        hasGift = 0

    return items, hasGift


def mailReceiveMail():
    
    data = request.data
    request_data = request.get_json()

    result = getItems(request_data, "mailId")

    data = {
        "items": result[0],
        "playerDataDelta": {
            "modified": {
                "consumable": {}, # TODO
                "inventory":{},
                "pushFlags": {
                    "hasGifts": result[1]
                },
                "status": {}
            },
            "deleted": {}
        }
    }

    return data


def mailReceiveAllMail():

    data = request.data
    request_data = request.get_json()

    result = getItems(request_data, "sysMailIdList")

    data = {
        "items": result[0],
        "playerDataDelta": {
            "modified": {
                "consumable": {}, # TODO
                "inventory":{},
                "pushFlags": {
                    "hasGifts": 0
                },
                "status": {}
            },
            "deleted": {}
        }
    }
    
    return data


def mailRemoveAllReceivedMail():
    
    global removeID

    data = request.data
    request_data = request.get_json()

    for ID in request_data["sysMailIdList"]:
        if ID not in removeID:
            removeID.append(ID)

    data = {
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data