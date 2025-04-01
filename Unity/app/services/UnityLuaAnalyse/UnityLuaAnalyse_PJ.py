from utils import pyServiceUtils
import os
import shutil
import sys
from utils import folderUtils
from Unity.app.services.UnityLuaAnalyse import UnityLuaAnalyse
from utils import sysUtils

from utils.CompanyUtil import Company_BB_Utils

projectPath = Company_BB_Utils.getDebugProjectFolderPath()
luaPath = os.path.join(projectPath, "Assets/Dev/Lua/")


# 打印 lua 文件夹的结构
# folderUtils.showFileStructureReg(luaPath, [".*\.lua$"])

def addStackLogBattle(svr_: UnityLuaAnalyse):
    _logFolderList = [
        "ui/page/Battle/",
        "Game/Module/Battle/",
    ]
    for _idx in range(len(_logFolderList)):
        _folderPath = sysUtils.folderPathFixEnd(os.path.join(luaPath, _logFolderList[_idx]))
        svr_.addLuaRunningStackLogInFolder(_folderPath)


def addStackLogFrameWork(svr_: UnityLuaAnalyse):
    _logFolderList = [
        # "Framework/Network/",
        # "Game/Common/",
        # "Game/Scene/",
        # "Game/Stage/",
        "Game/Module/logic/",
        "Game/Module/data/",
        "Game/Module/service/",
        "Game/Module/util/",
        # "net/",  # net/protobuflua/ 文件夹需要通过 Git 还原
        "ui/framework",
        "ui/page",
        "ui/util",
    ]
    for _idx in range(len(_logFolderList)):
        _folderPath = sysUtils.folderPathFixEnd(os.path.join(luaPath, _logFolderList[_idx]))
        svr_.addLuaRunningStackLogInFolder(_folderPath)


def addStackLogRichMan(svr_: UnityLuaAnalyse):
    _logFolderList = [
        "Game/Module/data/richMan/",
        "Game/Module/logic/richMan/",
        "Game/Module/service/richMan/",
        "ui/page/RichMan/",
        "Game/RichMan/",
    ]
    for _idx in range(len(_logFolderList)):
        _folderPath = sysUtils.folderPathFixEnd(os.path.join(luaPath, _logFolderList[_idx]))
        svr_.addLuaRunningStackLogInFolder(_folderPath)
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "Game/Module/logic/richMan/richManLogic.lua"))


def addStackLogBattle(svr_: UnityLuaAnalyse):
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "Game/Module/Battle/BattleEngine/"))


def addStackLogDailyDiscount(svr_: UnityLuaAnalyse):
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "ui/page/DailyDiscount/DailyDiscountPanel.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "Game/Module/data/dailyDiscount/dailyDiscountData.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "Game/Module/logic/dailyDiscount/dailyDiscountLogic.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "Game/Module/service/dailyDiscount/dailyDiscountService.lua"))


def addStackLogAll(svr_: UnityLuaAnalyse):
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "ui/"))
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "util/"))
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "Magic/"))
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "Framework/"))
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "platform/"))
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "Game/"))
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "UnityEngine/"))
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "ConfigScript/"))
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "common/"))
    svr_.addLuaRunningStackLogInFolder(os.path.join(luaPath, "ThirdParty/"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "GameInitPre.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "Init.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "net/NetRecord.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "net/ProtobufSerializer.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "net/ProtobufTypeManager.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "net/reconnect.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "net/socket_net.lua"))
    svr_.addLuaRunningStackLogOnFile(os.path.join(luaPath, "net/NetCodeManager.lua"))

if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)

    # addStackLogFrameWork(_svr)  # logic/data/service/ 日志
    # addStackLogRichMan(_svr) # 欢乐岛
    # addStackLogBattle(_svr)  # 战斗
    # addStackLogDailyDiscount(_svr)  # 每日特惠
    addStackLogAll(_svr)  # 所有加日志

    # _svr.addLuaRunningStackLogInFolder(luaPath)

    # 同步日志文件。
    # _svr.syncLogUtils(luaPath)
