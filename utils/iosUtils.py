from utils import cmdUtils
from utils import folderUtils
from utils import listUtils
from utils import sysUtils
from pathlib import Path
import utils.printUtils
import sys
import os


def isDeviceConnected():
    try:
        cmdUtils.doCmdAndGetPiplineList("ios-deploy", "--detect")
        return True
    except Exception as e:
        return False


# 判断是否有这个 appId_
def isAppIdExist(appId_: str):
    _pipline = cmdUtils.doCmdAndGetPiplineList("ios-deploy", "--list_bundle_id")
    for _idx in range(len(_pipline)):
        _bundleIdLine = _pipline[_idx]
        if str(_bundleIdLine).startswith("[....]"):  # 头两行不哟
            continue
        if _bundleIdLine == appId_:
            return True
    return False


# 获取文件列表
def getFileList(appId_: str, folderPathOnIphone_: str):
    _cmdStr = "ios-deploy --bundle_id '{0}' --list='{1}'".format(appId_, folderPathOnIphone_)
    print('_cmdStr = ' + str(_cmdStr))
    _pipline = cmdUtils.doStrAsCmdAndGetPipeline(_cmdStr, os.getcwd())

    _filePathList = []
    for _idx in range(len(_pipline)):
        _filePath = _pipline[_idx]
        if str(_filePath).startswith("[....]"):  # 头两行不哟
            continue
        if str(_filePath).endswith(os.path.sep):  # 文件夹不要
            continue
        _filePathList.append(_filePath)
    _filePathList.sort()
    return _filePathList


# 下载文件夹
def downloadFolder(appId_: str, folderPathOnIphone_: str, localFolderPath_: str):
    print("{0} {1} downloading...".format(appId_, folderPathOnIphone_))
    _filePathList = getFileList(appId_, folderPathOnIphone_)
    _fileLength = len(_filePathList)
    for _i in range(_fileLength):
        _filePath = _filePathList[_i]
        _cmdStr = "ios-deploy --download='{0}' --bundle_id '{1}' --to '{2}'".format(
            _filePath, appId_, localFolderPath_
        )
        print('\r', '    {}/{} {}'.format(_i + 1, _fileLength, _cmdStr), end='')
        cmdUtils.doStrAsCmdAndGetPipeline(_cmdStr, os.getcwd())
    print()


# 上传文件
def uploadFolder(localFolderPath_: str, appId_: str, folderPathOnIphone_: str):
    if not os.path.exists(localFolderPath_):
        utils.printUtils.pError("ERROR : {0} is not exist~!".format(localFolderPath_))
        sys.exit(1)
    _filePathList = folderUtils.getFileListInFolder(localFolderPath_)
    _localFolderPathSplitLen = len(Path(localFolderPath_).parts)
    _fileLength = len(_filePathList)
    for _i in range(_fileLength):
        _filePath = _filePathList[_i]
        _filePathSplitList = list(Path(_filePath).parts)
        listUtils.list_shift(_filePathSplitList, _localFolderPathSplitLen)
        _relativePath = listUtils.joinToStr(_filePathSplitList, os.path.sep)
        _targetPath = os.path.join(folderPathOnIphone_, _relativePath)
        _cmdStr = "ios-deploy --bundle_id '{0}' --upload '{1}' --to '{2}'".format(
            appId_, _filePath, _targetPath
        )
        print('\r', '    {}/{} {}'.format(_i + 1, _fileLength, _cmdStr), end='')
        cmdUtils.doStrAsCmdAndGetPipeline(_cmdStr, os.getcwd())
    print()


if __name__ == '__main__':
    _downloadFolderPath = "/Users/nobody/Downloads/iosContainerRes/"
    _sourceFolder = "/Documents/res/audio"
    _appId = "com.2x2.Skywire"

    if not isDeviceConnected():
        utils.printUtils.pError("ERROR - there is not device connected~!")
        sys.exit(1)

    if not isAppIdExist(_appId):
        utils.printUtils.pError("ERROR - {0} is not exist~!".format(_appId))
        sys.exit(1)
    # 下载到本地
    downloadFolder(_appId, _sourceFolder, _downloadFolderPath)
    # 在上传回去
    uploadFolder(sysUtils.pathJoin(_downloadFolderPath, _sourceFolder), _appId, _sourceFolder)
