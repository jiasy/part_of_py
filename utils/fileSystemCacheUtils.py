import os
import sys
from utils import fileUtils


# 获得文件修改时间的信息
def __getFileTimeCacheDict(folderPath_: str):
    _modifyTimeCachePath = os.path.join(folderPath_, ".modifyTimeCache")
    if not os.path.exists(_modifyTimeCachePath):
        return {}
    _lines = fileUtils.linesFromFile(_modifyTimeCachePath)
    # 解析 .createTime 文件内容，获取文件与其创建时间的字典
    _fileNameToCreateTimeDict = {}
    for _i in range(len(_lines)):
        _fileName, create_time_str = _lines[_i].split(" - ")
        _fileNameToCreateTimeDict[_fileName] = create_time_str
    return _fileNameToCreateTimeDict


def __get_fileNameList_folderNameList(folderPath_: str):
    _fileNameList = []
    _folderNameList = []
    for _fileOrFolderName in os.listdir(folderPath_):
        if _fileOrFolderName.startswith("."):
            continue
        _fileOrFolderPath = os.path.join(folderPath_, _fileOrFolderName)
        if os.path.isdir(_fileOrFolderPath):
            _folderNameList.append(_fileOrFolderName)
        elif os.path.isfile(_fileOrFolderPath):
            _fileNameList.append(_fileOrFolderName)
        else:
            print(f"ERROR : {os.path.join(folderPath_, _fileOrFolderName)} is not file or dir?")
    return _fileNameList, _folderNameList


# 确保有文件修改时间的缓存
def __makeSureCreateTimeCacheExist(folderPath_: str, createFolderList_=None):
    if createFolderList_ is None:  # 根节点，创建
        createFolderList_ = []
    _fileNameList, _folderNameList = __get_fileNameList_folderNameList(folderPath_)
    if not os.path.exists(os.path.join(folderPath_, ".modifyTimeCache")):  # 创建 .modifyTimeCache 文件并写入内容
        updateFileChangeTimeCache(folderPath_)
    for _i in range(len(_folderNameList)):
        __makeSureCreateTimeCacheExist(os.path.join(folderPath_, _folderNameList[_i]), createFolderList_)
    return createFolderList_


# 得到当前文件夹内的变更文件列表
def __getFileChangeList(folderPath_: str):
    _fileNameList, _folderNameList = __get_fileNameList_folderNameList(folderPath_)
    _fileNameToCreateTimeDict = __getFileTimeCacheDict(folderPath_)
    _updatedFileList = []  # 变更列表
    for _i in range(len(_fileNameList)):
        _fileName = _fileNameList[_i]  # 文件
        _curTime = os.path.getmtime(os.path.join(folderPath_, _fileName))
        if _fileName in _fileNameToCreateTimeDict:  # 记录过时间，比较
            _oldTime = float(_fileNameToCreateTimeDict[_fileName])
            if _curTime != _oldTime:  # 不一样需要更新
                _fileNameToCreateTimeDict[_fileName] = _curTime
                _updatedFileList.append(os.path.join(folderPath_, _fileName))
        else:  # 没记录过，记录一下
            _fileNameToCreateTimeDict[_fileName] = _curTime
            _updatedFileList.append(os.path.join(folderPath_, _fileName))
    return _updatedFileList


# 获取变更了的时间
def getFileChangeListDeep(folderPath_: str, updateFileList_: list = None, createCacheFolderList_: list = None):
    # 根节点，操作
    if updateFileList_ is None:
        updateFileList_ = []
    if createCacheFolderList_ is None:
        createCacheFolderList_ = __makeSureCreateTimeCacheExist(folderPath_)  # 返回新创建的文件夹列表

    _fileNameList, _folderNameList = __get_fileNameList_folderNameList(folderPath_)

    _isCreate = False  # 是不是刚创建的
    for _i in range(len(createCacheFolderList_)):  # 遍历刚创建的
        if os.path.samefile(folderPath_, createCacheFolderList_[_i]):  # 在其中
            _isCreate = True  # 那就是刚创建的

    if not _isCreate:  # 不是刚创建的，比较当前和记录
        updateFileList_.extend(__getFileChangeList(folderPath_))  # 记录变更的
    else:  # 是刚创建的，直接就加进来
        for _i in range(len(_fileNameList)):
            updateFileList_.append(os.path.join(folderPath_, _fileNameList[_i]))

    # 其下的文件夹继续进行缓存
    for _i in range(len(_folderNameList)):
        _folderPath = os.path.join(folderPath_, _fileNameList[_i])
        getFileChangeListDeep(_folderPath, updateFileList_, createCacheFolderList_)

    return updateFileList_


# 更新文件夹内的修改时间缓存
def updateFileChangeTimeCache(folderPath_: str):
    _modifyTimeCachePath = os.path.join(folderPath_, ".modifyTimeCache")
    _fileNameList, _folderNameList = __get_fileNameList_folderNameList(folderPath_)
    _createTimeTxt = "\n".join([f"{_fileName} - {os.path.getmtime(os.path.join(folderPath_, _fileName))}" for _fileName in _fileNameList])
    fileUtils.writeFileWithStr(_modifyTimeCachePath, _createTimeTxt)
    for _i in range(len(_folderNameList)):
        updateFileChangeTimeCache(os.path.join(folderPath_, _folderNameList[_i]))


# 文件是否变更过
def isFileChanged(filePath_: str):
    _folderPathAndFileName = os.path.split(filePath_)
    _folderPath = _folderPathAndFileName[0]
    _fileName = _folderPathAndFileName[1]
    _fileTimeCacheDict = __getFileTimeCacheDict(filePath_)
    if _fileName in _fileTimeCacheDict:
        return _fileTimeCacheDict[_fileName] == os.path.getmtime(filePath_)
    return True


if __name__ == "__main__":
    from utils.CompanyUtil import Company_BB_Utils
    import os

    # updateFileChangeTimeCache(os.path.join(Company_BB_Utils.getSLGProjectPath(),"svn_repos/trunk/design/"))
    # sys.exit(1)
    _updateFileList = getFileChangeListDeep(os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel/"))
    print(_updateFileList)
