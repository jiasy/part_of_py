from utils import pyServiceUtils
from Unity.app.services.UnityCSharpAnalyse import UnityCSharpAnalyse


def addStackLog_DataUIBinder(svr_: UnityCSharpAnalyse):
    _baseFolderPath = "/Volumes/Files/develop/selfDevelop/Unity/DataCenter/DataCenter/Assets/"
    _folderPathList = [
        "DataUIBinder/Test/",
        "DataUIBinder/UI/",
    ]

    for _idx in range(len(_folderPathList)):
        _targetFolder = _baseFolderPath + _folderPathList[_idx]
        svr_.addRunningStackLog(_targetFolder, [])


if __name__ == '__main__':
    _unityCSharpAnalyse = pyServiceUtils.getSvr(__file__)
    addStackLog_DataUIBinder(_unityCSharpAnalyse)
