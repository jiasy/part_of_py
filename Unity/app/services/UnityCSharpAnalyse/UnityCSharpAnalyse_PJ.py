from utils import pyServiceUtils
import os
import shutil
from Unity.app.services.UnityCSharpAnalyse import UnityCSharpAnalyse
import sys
from utils import folderUtils
import os
from utils.CompanyUtil import Company_BB_Utils

assetsPath = os.path.join(Company_BB_Utils.getDebugProjectFolderPath(), "Assets/")


# 获取文件夹下，哪里有cs文件，然后再确认那些是需要打日志的。
# folderUtils.getTypeLocateInfoInFolder(assetsPath, ".cs")
# Artwork
# Plugins
# Wwise
# Addons
# Scripts-Public
# FightDemo
# Scripts
# GameResources
# AssetManager
# Editor


def addStackLog_FightDemo(svr_: UnityCSharpAnalyse):
    svr_.addRunningStackLog(
        assetsPath + "FightDemo/", [
            "Plugins/ThirdParty/",  # 排除
            "HydroformDemo.cs"  # 排除
        ]
    )


def addStackLog_Scripts(svr_: UnityCSharpAnalyse):
    svr_.addRunningStackLog(
        assetsPath + "Scripts/", [
            "ThirdParty/",  # XLua/Gen 等
            "Framework/UI/Editor/",  # 排除
            "Pb/",  # 排除
            "Framework/ConfigManager/ConfigUtil/JSON/",
            "Framework/Lua/Editor/",
            "BabeltimeSDK/",
        ]
    )

    # svr_.addRunningStackLog(
    #     assetsPath + "Scripts/ThirdParty/", [
    #         "ICSharpCode.SharpZipLib/"  # 排除
    #     ]
    # )L


def addStackLog_AssetManager(svr_: UnityCSharpAnalyse):
    svr_.addRunningStackLog(
        assetsPath + "AssetManager/", [
        ]
    )


def addStackLog_ScriptsPublic(svr_: UnityCSharpAnalyse):
    svr_.addRunningStackLog(
        assetsPath + "Scripts-Public/", [
            "Tools/SceneEditor/Editor/Lo"
        ]
    )


def addStackLog_GameResources(svr_: UnityCSharpAnalyse):
    svr_.addRunningStackLog(
        assetsPath + "GameResources/", [
        ]
    )


def addStackLog_Addons(svr_: UnityCSharpAnalyse):
    svr_.addRunningStackLog(
        assetsPath + "Addons/", [
        ]
    )


def addStackLog_Plugins(svr_: UnityCSharpAnalyse):
    svr_.addRunningStackLog(
        assetsPath + "Plugins/ThirdParty/URPWater/", [
        ]
    )

    svr_.addRunningStackLog(
        assetsPath + "Plugins/ThirdParty/ProtobufDotNet/", [
        ]
    )

    svr_.addRunningStackLog(
        assetsPath + "Plugins/ThirdParty/AVProVideo/", [
        ]
    )

    svr_.addRunningStackLog(
        assetsPath + "Plugins/ThirdParty/StylizedWater2/", [
        ]
    )


def addStackLog_UI(svr_: UnityCSharpAnalyse):
    svr_.addRunningStackLog(
        assetsPath + "Scripts/Framework/UI/", [
            "Scripts/Framework/UI/Editor/",  # 排除
        ]
    )


if __name__ == '__main__':
    _unityCSharpAnalyse = pyServiceUtils.getSvr(__file__)

    # _unityCSharpAnalyse.addRunningStackLog(
    #     assetsPath + "Scripts/Framework/UI/", [
    #         "Scripts/Framework/UI/Editor/",  # 排除
    #     ]
    # )
    # sys.exit(1)

    # folderUtils.getTypeLocateInfoInFolder(assetsPath, ".cs")
    # sys.exit(1)

    # addStackLog_FightDemo(_unityCSharpAnalyse)
    addStackLog_Scripts(_unityCSharpAnalyse)
    addStackLog_ScriptsPublic(_unityCSharpAnalyse)
    addStackLog_GameResources(_unityCSharpAnalyse)
    # addStackLog_Addons(_unityCSharpAnalyse)
    # addStackLog_Plugins(_unityCSharpAnalyse)
    addStackLog_UI(_unityCSharpAnalyse)

    # # 同步日志文件。
    # _unityCSharpAnalyse.syncLogUtils(assetsPath)
