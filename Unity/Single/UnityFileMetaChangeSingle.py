# !/usr/bin/env python3
import os
import sys
import yaml
import chardet


def os_is_win32():
    return sys.platform == 'win32'


def folderPathFixEnd(path_str):
    if not os_is_win32():
        if not path_str[-1] == "/":
            return path_str + "/"
        else:
            return path_str
    if path_str.startswith("\\\\?\\"):
        return path_str
    ret = "\\\\?\\" + os.path.abspath(path_str)
    ret = ret.replace("//", "/")
    ret = ret.replace("/", "\\")
    return ret


def gci(folderPath_: str, fileFilter_: list, fileList_: list = None):
    if not os.path.isdir(folderPath_):
        sys.exit(1)
    files = os.listdir(folderPath_)
    for fi in files:
        fi_d = os.path.join(folderPath_, fi)
        if os.path.isdir(fi_d):
            gci(fi_d, fileFilter_, fileList_)
        else:
            _filePath = os.path.join(folderPath_, fi_d)
            _fileSuffix = os.path.splitext(_filePath)[1]
            if fileFilter_:
                if _filePath and not _fileSuffix == "" and (_fileSuffix in fileFilter_):
                    fileList_.append(_filePath)
            else:
                fileList_.append(_filePath)


def getFileListInFolder(folder_: str, filters_: list = None):
    _filePathList = []
    folder_ = folderPathFixEnd(folder_)
    if filters_ and len(filters_) > 0:
        for _i in range(len(filters_)):
            if filters_[_i] == "" or not filters_[_i][0] == ".":
                raise Exception("后缀不对")
                return None
    gci(
        folder_,
        filters_,
        _filePathList
    )
    return _filePathList


def getRelativePathToMetaDict(assetsPath_):
    _filePathList = getFileListInFolder(
        assetsPath_,
        [".png", ".jpg", ".mat", ".prefab", ".controller", ".anim", ".FBX", ".PNG", ".physicsMaterial2D"]
    )
    _relativePathToGuidDict = {}
    for _i in range(len(_filePathList)):
        _filePath = _filePathList[_i]
        _metaFilePath = _filePath + ".meta"
        _fs = open(_metaFilePath, encoding="UTF-8")
        _yamlData = yaml.load(_fs, Loader=yaml.FullLoader)
        _relativePath = _filePath.split(assetsPath_)[1]
        _relativePathToGuidDict[_relativePath] = _yamlData.guid
    return _relativePathToGuidDict


def getAllKnowTypeFileInAssets(assetsPath_):
    return getFileListInFolder(
        assetsPath_,
        [".meta", ".mat", ".prefab", ".controller", ".anim", ".renderTexture", ".asset", ".fontsettings",
         ".physicsMaterial2D"]
    )


def readFromFile(filePath_: str):
    _encodeInfo = None
    try:
        _file = open(filePath_, 'rb')
        try:
            _encodeInfo = chardet.detect(_file.read())
        finally:
            _file.close()
    except Exception as e:
        print(filePath_, e)

    _encodeType = _encodeInfo["encoding"]
    _contentStr = None
    try:
        _file = open(file=filePath_, mode='r', encoding=_encodeType)
        try:
            _contentStr = _file.read()
        finally:
            _file.close()
    except Exception as e:
        print(filePath_, e)
        sys.exit(1)
    return _contentStr, _encodeType


def writeFileWithStr(filePath_: str, str_: str, encodeType_: str):
    if not os.path.exists(os.path.dirname(filePath_)):
        os.makedirs(os.path.dirname(filePath_))
    try:
        _file = open(file=filePath_, mode='w', encoding=encodeType_)
        try:
            _file.write(str_)
        finally:
            _file.close()
    except Exception as e:
        print(filePath_, e)


if __name__ == "__main__":
    # 程序工程 - 美术资源文件的相对路径和guid之间的关系
    _developAssetsPath = "/disk/file/GIT/A/m3d/Assets/AssetsA/"
    _developRelativePathToGuidDict = getRelativePathToMetaDict(_developAssetsPath)

    # 美术工程 - 资源文件相对路径和guid之间的关系
    _artAssetsPath = "/disk/file/GIT/A/m3d/Assets/AssetsA/"
    _artRelativePathToGuidDict = getRelativePathToMetaDict(_artAssetsPath)

    # 美术工程，相同的相对路径guid的映射关系
    _inDevelopNotInArtList = []
    _inArtNotInDevelopList = []
    _artGuidToDevelopGuidDict = {}
    for _developRelativePath in _developRelativePathToGuidDict:
        if _developRelativePath in _artRelativePathToGuidDict:
            _guidInDevelop = _developRelativePathToGuidDict[_developRelativePath]
            _guidInArt = _artGuidToDevelopGuidDict[_developRelativePath]
            if not _guidInDevelop == _guidInArt:
                _artGuidToDevelopGuidDict[_guidInArt] = _guidInDevelop
        else:
            _inDevelopNotInArtList.append(_developRelativePath)

    for _artRelativePath in _artRelativePathToGuidDict:
        if not _artRelativePath in _developRelativePathToGuidDict:
            _inArtNotInDevelopList.append(_artRelativePath)

    # 打印两者差异
    print("在 开发 目录，不在 美术 目录 的文件有 : ")
    for _i in range(len(_inDevelopNotInArtList)):
        print("   " + _inDevelopNotInArtList[_i])
    print("在 美术 目录，不在 开发 目录 的文件有 : ")
    for _i in range(len(_inArtNotInDevelopList)):
        print("   " + _inArtNotInDevelopList[_i])

    # 打开美术工程，把所有的guid全部替换掉
    _artFilePathList = getAllKnowTypeFileInAssets(_artAssetsPath)
    for _i in range(len(_artFilePathList)):
        _artFilePath = _artFilePathList[_i]
        _contentStr, _encodeType = readFromFile(_artFilePath)
        for _key in _artGuidToDevelopGuidDict:
            _contentStr.replace(_key, _artGuidToDevelopGuidDict[_key])
        writeFileWithStr(_artFilePath, _contentStr, _encodeType)
