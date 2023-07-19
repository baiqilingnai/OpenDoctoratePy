import re
import logging
from datetime import datetime

from flask import Flask

from utils import read_json
from constants import CONFIG_PATH

import account, background, building, campaignV2, char, charBuild, charm, \
        crisis, deepsea, mail, online, tower, quest, pay, rlv2, shop, story, \
        user, asset.assetbundle, config.prod

server_config = read_json(CONFIG_PATH)

app = Flask(__name__)
host = server_config["server"]["host"]
port = server_config["server"]["port"]

logger = logging.getLogger('werkzeug')
logger.setLevel(logging.INFO)
logger.addFilter(lambda s: not re.match(".*404 -*", s.getMessage()))

app.add_url_rule('/app/getSettings', methods=['POST'], view_func=user.appGetSettings)
app.add_url_rule('/app/getCode', methods=['POST'], view_func=user.appGetCode)

app.add_url_rule('/account/login', methods=['POST'], view_func=account.accountLogin)
app.add_url_rule('/account/syncData', methods=['POST'], view_func=account.accountSyncData)
app.add_url_rule('/account/syncStatus', methods=['POST'], view_func=account.accountSyncStatus)
app.add_url_rule('/account/yostar_auth_request', methods=['POST'], view_func=account.accountYostarAuthRequest)
app.add_url_rule('/account/yostar_auth_submit', methods=['POST'], view_func=account.accountYostarAuthSubmit)

app.add_url_rule('/assetbundle/official/Android/assets/<string:assetsHash>/<string:fileName>', methods=['GET'], view_func=asset.assetbundle.getFile)

app.add_url_rule('/background/setBackground', methods=['POST'], view_func=background.backgroundSetBackground)

app.add_url_rule('/building/sync', methods=['POST'], view_func=building.buildingSync)

app.add_url_rule('/campaignV2/battleStart', methods=['POST'], view_func=campaignV2.campaignV2BattleStart)
app.add_url_rule('/campaignV2/battleFinish', methods=['POST'], view_func=campaignV2.campaignV2BattleFinish)
app.add_url_rule('/campaignV2/battleSweep', methods=['POST'], view_func=campaignV2.campaignV2BattleSweep)

app.add_url_rule('/char/changeMarkStar', methods=['POST'], view_func=char.charChangeMarkStar)

app.add_url_rule('/charBuild/addonStage/battleStart', methods=['POST'], view_func=quest.questBattleStart)
app.add_url_rule('/charBuild/addonStage/battleFinish', methods=['POST'], view_func=quest.questBattleFinish)
app.add_url_rule('/charBuild/addonStory/unlock', methods=['POST'], view_func=charBuild.charBuildaddonStoryUnlock)
app.add_url_rule('/charBuild/batchSetCharVoiceLan', methods=['POST'], view_func=charBuild.charBuildBatchSetCharVoiceLan)
app.add_url_rule('/charBuild/setCharVoiceLan', methods=['POST'], view_func=charBuild.charBuildSetCharVoiceLan)
app.add_url_rule('/charBuild/setDefaultSkill', methods=['POST'], view_func=charBuild.charBuildSetDefaultSkill)
app.add_url_rule('/charBuild/changeCharSkin', methods=['POST'], view_func=charBuild.charBuildChangeCharSkin)
app.add_url_rule('/charBuild/setEquipment', methods=['POST'], view_func=charBuild.charBuildSetEquipment)
app.add_url_rule('/charBuild/changeCharTemplate', methods=['POST'], view_func=charBuild.charBuildChangeCharTemplate)

app.add_url_rule('/charm/setSquad', methods=['POST'], view_func=charm.charmSetSquad)

app.add_url_rule('/config/prod/announce_meta/Android/preannouncement.meta.json', methods=['GET'], view_func=config.prod.prodPreAnnouncement)
app.add_url_rule('/config/prod/announce_meta/Android/announcement.meta.json', methods=['GET'], view_func=config.prod.prodAnnouncement)
app.add_url_rule('/config/prod/official/Android/version', methods=['GET'], view_func=config.prod.prodAndroidVersion)
app.add_url_rule('/config/prod/official/network_config', methods=['GET'], view_func=config.prod.prodNetworkConfig)
app.add_url_rule('/config/prod/official/refresh_config', methods=['GET'], view_func=config.prod.prodRefreshConfig)
app.add_url_rule('/config/prod/official/remote_config', methods=['GET'], view_func=config.prod.prodRemoteConfig)

app.add_url_rule('/crisis/getInfo', methods=['POST'], view_func=crisis.crisisGetCrisisInfo)
app.add_url_rule('/crisis/battleStart', methods=['POST'], view_func=crisis.crisisBattleStart)
app.add_url_rule('/crisis/battleFinish', methods=['POST'], view_func=crisis.crisisBattleFinish)

app.add_url_rule('/deepSea/branch', methods=['POST'], view_func=deepsea.deepSeaBranch)
app.add_url_rule('/deepSea/event', methods=['POST'], view_func=deepsea.deepSeaEvent)

app.add_url_rule('/mail/getMetaInfoList', methods=['POST'], view_func=mail.mailGetMetaInfoList)
app.add_url_rule('/mail/listMailBox', methods=['POST'], view_func=mail.mailListMailBox)
app.add_url_rule('/mail/receiveMail', methods=['POST'], view_func=mail.mailReceiveMail)
app.add_url_rule('/mail/receiveAllMail', methods=['POST'], view_func=mail.mailReceiveAllMail)
app.add_url_rule('/mail/removeAllReceivedMail', methods=['POST'], view_func=mail.mailRemoveAllReceivedMail)

app.add_url_rule('/online/v1/ping', methods=['POST'], view_func=online.onlineV1Ping)
app.add_url_rule('/online/v1/loginout', methods=['POST'], view_func=online.onlineV1LoginOut)

app.add_url_rule('/tower/createGame', methods=['POST'], view_func=tower.towerCreateGame)
app.add_url_rule('/tower/initGodCard', methods=['POST'], view_func=tower.towerInitGodCard)
app.add_url_rule('/tower/initGame', methods=['POST'], view_func=tower.towerInitGame)
app.add_url_rule('/tower/initCard', methods=['POST'], view_func=tower.towerInitCard)
app.add_url_rule('/tower/battleStart', methods=['POST'], view_func=tower.towerBattleStart)
app.add_url_rule('/tower/battleFinish', methods=['POST'], view_func=tower.towerBattleFinish)
app.add_url_rule('/tower/recruit', methods=['POST'], view_func=tower.towerRecruit)
app.add_url_rule('/tower/chooseSubGodCard', methods=['POST'], view_func=tower.towerChooseSubGodCard)
app.add_url_rule('/tower/settleGame', methods=['POST'], view_func=tower.towerSettleGame)

app.add_url_rule('/pay/getUnconfirmedOrderIdList', methods=['POST'], view_func=pay.payGetUnconfirmedOrderIdList)
app.add_url_rule('/u8/pay/getAllProductList', methods=['POST'], view_func=pay.paygetAllProductList)

app.add_url_rule('/quest/battleStart', methods=['POST'], view_func=quest.questBattleStart)
app.add_url_rule('/quest/battleFinish', methods=['POST'], view_func=quest.questBattleFinish)
app.add_url_rule('/quest/saveBattleReplay', methods=['POST'], view_func=quest.questSaveBattleReplay)
app.add_url_rule('/quest/getBattleReplay', methods=['POST'], view_func=quest.questGetBattleReplay)
app.add_url_rule('/quest/changeSquadName', methods=['POST'], view_func=quest.questChangeSquadName)
app.add_url_rule('/quest/squadFormation', methods=['POST'], view_func=quest.questSquadFormation)
app.add_url_rule('/quest/getAssistList', methods=['POST'], view_func=quest.questGetAssistList)

app.add_url_rule('/rlv2/createGame', methods=['POST'], view_func=rlv2.rlv2CreateGame)
app.add_url_rule('/rlv2/chooseInitialRelic', methods=['POST'], view_func=rlv2.rlv2ChooseInitialRelic)
app.add_url_rule('/rlv2/selectChoice', methods=['POST'], view_func=rlv2.rlv2SelectChoice)
app.add_url_rule('/rlv2/chooseInitialRecruitSet', methods=['POST'], view_func=rlv2.rlv2ChooseInitialRecruitSet)
app.add_url_rule('/rlv2/activeRecruitTicket', methods=['POST'], view_func=rlv2.rlv2ActiveRecruitTicket)
app.add_url_rule('/rlv2/recruitChar', methods=['POST'], view_func=rlv2.rlv2RecruitChar)
app.add_url_rule('/rlv2/closeRecruitTicket', methods=['POST'], view_func=rlv2.rlv2CloseRecruitTicket)
app.add_url_rule('/rlv2/finishEvent', methods=['POST'], view_func=rlv2.rlv2FinishEvent)
app.add_url_rule('/rlv2/moveAndBattleStart', methods=['POST'], view_func=rlv2.rlv2MoveAndBattleStart)

app.add_url_rule('/shop/getSkinGoodList', methods=['POST'], view_func=shop.shopGetSkinGoodList)

app.add_url_rule('/story/finishStory', methods=['POST'], view_func=story.storyFinishStory)
app.add_url_rule('/quest/finishStoryStage', methods=['POST'], view_func=story.storyFinishStory)

app.add_url_rule('/user/auth', methods=['POST'], view_func=user.userAuth)
app.add_url_rule('/user/agreement', methods=['GET'], view_func=user.userAgreement)
app.add_url_rule('/user/checkIn', methods=['POST'], view_func=user.userCheckIn)
app.add_url_rule('/user/changeSecretary', methods=['POST'], view_func=user.userChangeSecretary)
app.add_url_rule('/user/login', methods=['POST'], view_func=user.userLogin)
app.add_url_rule('/user/changeAvatar', methods=['POST'], view_func=user.userChangeAvatar)
app.add_url_rule('/user/oauth2/v1/grant', methods=['POST'], view_func=user.userOAuth2V1Grant)
app.add_url_rule('/user/info/v1/need_cloud_auth', methods=['POST'], view_func=user.userV1NeedCloudAuth)
app.add_url_rule('/user/yostar_createlogin', methods=['POST'], view_func=user.userYostarCreatelogin)
app.add_url_rule('/u8/user/v1/getToken', methods=['POST'], view_func=user.userV1getToken)

app.add_url_rule(
    '/user/auth/v1/token_by_phone_password',
    methods=['POST'], view_func=user.auth_v1_token_by_phone_password
)
app.add_url_rule(
    '/user/info/v1/basic',
    methods=['GET'], view_func=user.info_v1_basic
)
app.add_url_rule(
    '/user/oauth2/v2/grant',
    methods=['POST'], view_func=user.oauth2_v2_grant
)
app.add_url_rule(
    '/app/v1/config',
    methods=['GET'], view_func=user.app_v1_config
)
app.add_url_rule(
    '/general/v1/server_time',
    methods=['GET'], view_func=user.general_v1_server_time
)


def writeLog(data):
    print(f'[{datetime.utcnow()}] {data}')

if __name__ == "__main__":
    writeLog('[SERVER] Server started at http://' + host + ":" + str(port))
    app.run(host=host, port=port, debug=True)