from utils import pyServiceUtils
from Unity.app.services.UnityCSharpAnalyse import UnityCSharpAnalyse
import os


def addStackLog_XM(svr_: UnityCSharpAnalyse):
    _targetFolder = "/disk/file/GIT/A/m3d/Assets/AssetsA/"
    svr_.addRunningStackLog(
        _targetFolder, [
            "3rd/FindReference2/Editor/Script/FR2_Asset.cs",
        ]
    )


def addStackLog_BY(svr_: UnityCSharpAnalyse):
    _baseFolderPath = "/disk/file/GIT/A/m3d/Assets/AssetsFish/"

    _folderPathList = [
        "Plugins/MotionFramework/",
        "MotionExtension/",
    ]

    for _idx in range(len(_folderPathList)):
        _targetFolder = _baseFolderPath + os.sep + _folderPathList[_idx]
        svr_.addRunningStackLog(_targetFolder, [])


if __name__ == '__main__':
    _unityCSharpAnalyse = pyServiceUtils.getSvr(__file__)

    # addStackLog_BY(_unityCSharpAnalyse)
    # addStackLog_XM(_unityCSharpAnalyse)
