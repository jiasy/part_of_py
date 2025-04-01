# !/usr/bin/env python3
import utils.fileUtils
import utils.strUtils
import utils.listUtils
import utils.sysUtils
import utils.printUtils
import shutil
import sys
import re
from pathlib import Path


# 移除UTF-8文件的BOM字节
def removeBomInUTF8(folderPath_: str, suffix_: str):
    for _filePath in getFilePathWithSuffixInFolder(folderPath_, suffix_):
        utils.fileUtils.removeBomInUTF8(_filePath)


# 显示文件夹结构 有正则过滤
def showFileStructureReg(path_: str, reStrList_: list = None, needPrintFolder_: bool = False, depth_: int = 0):
    # 删


# 显示文件结构
def showFileStructure(path_: str, prefix_: str = "", excludeFolderList_: list[str] = [], showFiles_: bool = True, depth_: int = 0):
    # 删


# 显示文件夹结构
def showFolderStructure(path_: str, prefix_: str = "", excludeFolderList_: list[str] = []):
    showFileStructure(path_, prefix_, excludeFolderList_, False, 0)


# 显示指定文件的结构
def getFileStructure(path_: str, filterList_: list, fileStruct_: dict = None, depth_: int = 0):
    # 删
    return fileStruct_


# 只获取文件夹
def getFolderList(path_: str, folderList_: list = None):
    _folderList = folderList_
    if _folderList == None:
        _folderList = []
    for _item in os.listdir(path_):
        _newitem = os.path.join(path_, _item)
        if os.path.isdir(_newitem):
            _folderList.append(_newitem)
            getFolderList(_newitem, _folderList)
    return _folderList


# 一层文件中，删除空文件夹
def deleteBlankFolderJustOneDepth(path_: str):
    _folderList = getFolderNameListJustOneDepth(path_)
    for _i in range(len(_folderList)):
        _folderPath = os.path.join(path_, _folderList[_i])
        if len(os.listdir(_folderPath)) == 0:
            os.removedirs(_folderPath)
            print('remove folder : ' + str(_folderPath))


# 获取文件夹 仅仅 一层文件夹
def getFolderNameListJustOneDepth(path_: str):
    _folderList = []
    if os.path.exists(path_) is False:
        print(f"ERROR : not exist - {path_}")
        sys.exit(1)
    for _item in os.listdir(path_):
        _filePath = os.path.join(path_, _item)
        if os.path.isdir(_filePath):
            _folderList.append(_item)
    return _folderList


# 仅仅获取第一层的 文件名（含后缀）
def getFileNameListJustOneDepth(path_: str, fileFilter_: list = None):
    _fileList = []
    for _item in os.listdir(path_):
        _filePath = os.path.join(path_, _item)
        if not os.path.isdir(_filePath):
            if fileFilter_:  # 过滤的后缀列表
                _fileSuffix = os.path.splitext(_filePath)[1]  # 当前的文件，后缀名
                if _filePath and not _fileSuffix == "" and (_fileSuffix in fileFilter_):
                    _fileList.append(_item)
            else:  # 没有需要过滤的后缀列表，就全部记录下来
                _fileList.append(_item)
    return _fileList


# 保存文件之前先判断此文件是否存在，如果不存在，先创建父文件夹
def makeSureDirIsExists(path_: str):
    # 路径存在
    if os.path.exists(path_):
        # 不是文件夹，返回False
        if not os.path.isdir(path_):
            print("路径 " + path_ + " 存在，但不是一个文件夹。")
            return False
        else:
            return True
    else:
        os.makedirs(path_)


# 删除并重新创建
def deleteThenCreateFolder(path_: str):
    if os.path.exists(path_):
        utils.folderUtils.removeTree(path_)
    utils.folderUtils.makeSureDirIsExists(path_)


# 通过 后缀 列表，删除文件[".xx"]
def removeFileByFilter(folderPath_: str, fileFilter_: list):
    _filePathList = getFileListInFolder(folderPath_, fileFilter_)
    for _i in range(len(_filePathList)):
        utils.fileUtils.removeExistFile(_filePathList[_i])


# 获取某一类型的文件的大小总和
def getFileSizeInFolder(folderPath_: str, filters_: list):
    _filePathList = getFileListInFolder(folderPath_, filters_)
    _totalSize = 0
    for _i in range(len(_filePathList)):
        _totalSize = _totalSize + utils.fileUtils.getFileSize(_filePathList[_i])
    return _totalSize


# 在这个文件夹中，类型列表中的每一个类型大小各自为多少
def getFileSizeInFolderByTypes(folderPath_: str, types_: list):
    _totalSize = 0
    for _i in range(len(types_)):
        _fileType = types_[_i]
        _fileSizes = getFileSizeInFolder(folderPath_, [_fileType])
        _currentSize = _fileSizes / 1024 / 1024
        _totalSize = _totalSize + _currentSize
        print(_fileType + " : " + '%.2f' % _currentSize + " MB")
    print("all : " + '%.2f' % _totalSize + " MB")


# 将文件夹内指定文件类型进行大小排序显示
def getFileSizeInfoSortList(folderPath_: str, filters_: list):
    _filePathList = getFileListInFolder(folderPath_, filters_)
    _fileSizeInfoList = getFileSizeInfoSortListByFileList(_filePathList)
    return _fileSizeInfoList


# 根据给的文件列表，按大小排序输出文件信息
def getFileSizeInfoSortListByFileList(filePathList_):
    _totalSize = 0
    _fileSizeInfoList = []
    for _i in range(len(filePathList_)):
        _fileInfo = {}
        _fileSize = utils.fileUtils.getFileSize(filePathList_[_i])
        _fileInfo["size"] = _fileSize
        _totalSize = _totalSize + _fileSize
        _fileInfo["filePath"] = filePathList_[_i]
        _fileSizeInfoList.append(_fileInfo)
    # SAMPLE - 字典排序
    utils.listUtils.sortListOfDict(_fileSizeInfoList, "size", True)

    for _i in range(len(_fileSizeInfoList)):
        _filePath = _fileSizeInfoList[_i]["filePath"]
        _fileSize = _fileSizeInfoList[_i]["size"] / 1024
        print(str(round(_fileSize, 2)) + "KB : " + _filePath)
    print(str(round(_totalSize, 2) / (1024 * 1024)) + "MB")
    return _fileSizeInfoList


# 获取 suffix_ 类型在 folderPath_ 中都分布在那几个文件夹。
def getTypeLocateInfoInFolder(folderPath_: str, suffix_: str, justOneDepth_: bool):
    _folderSplitLen = len(Path(folderPath_).parts)
    _filePathList = getFileListInFolder(folderPath_, [suffix_])
    _folderPathList = []
    for _i in range(len(_filePathList)):
        _filePathSplit = Path(_filePathList[_i]).parts
        _filePathSplitList = list(_filePathSplit)
        utils.listUtils.list_shift(_filePathSplitList, _folderSplitLen)
        _relativePath = utils.listUtils.joinToStr(_filePathSplitList, os.path.sep)  # 获得相对路径
        _relativeFolderPath = os.path.split(_relativePath)[0]
        if _relativeFolderPath != "":
            _folderPathList.append(_relativeFolderPath)  # 获得所在文件夹
    if justOneDepth_:  # 只获得最上面的一层信息
        _folderPathList = list(set(_folderPathList))  # 去重 再 转回 列表
        for _i in range(len(_folderPathList)):
            _folderPathList[_i] = Path(_folderPathList[_i]).parts[0]

    _folderPathList = list(set(_folderPathList))  # 去重 再 转回 列表
    _folderPathList.sort()
    return _folderPathList


# 在这个文件夹中，每一类文件占多少空间
def getFolderSizeInfo(folderPath_: str):
    getFileSizeInFolderByTypes(folderPath_, getSuffixsInFolder(folderPath_))


# 获取 文件夹内所有文件的后缀集合
def getSuffixsInFolder(filePath_: str):
    # 后缀名集合
    _suffixList = []
    # 文件夹内所有的文件
    _fileList = getFileListInFolder(filePath_)
    for _i in range(len(_fileList)):
        _filePath = _fileList[_i]
        _suffix = utils.fileUtils.getSuffix(_filePath)
        if not _suffix == "" and not (_suffix in _suffixList):
            _suffixList.append(_suffix)  # 记录后缀
    return _suffixList


# 获取文件夹中，给定后缀的文件路径列表
def getFilePathWithSuffixInFolder(filePath_: str, suffix_: str):
    # 文件夹内所有的文件
    _fileList = getFileListInFolder(filePath_)
    _fileWithSuffixList = []
    for _i in range(len(_fileList)):
        _filePath = _fileList[_i]
        _suffix = utils.fileUtils.getSuffix(_filePath)
        if _suffix.lower() == suffix_.lower():
            _fileWithSuffixList.append(_filePath)
    return _fileWithSuffixList


# 遍历文件夹，按照后缀获取文件列表
def gci(folderPath_: str, fileFilters_: list, filePathList_: list, isMain_=True):
    # 递归第一层处理，后缀过滤表
    if isMain_ and fileFilters_ is not None:
        fileFilters_ = suffixFiltersCheckAndUpper(fileFilters_)  # 后缀名，大写
        if fileFilters_ is None:
            utils.printUtils.pError("ERROR 后缀过滤列表中出现不符合条件的元素")
            sys.exit(1)
    # 判断路径的可靠性
    if not os.path.isdir(folderPath_):
        utils.printUtils.pError("ERROR 不是目录 : " + folderPath_)
        sys.exit(1)
    # 遍历 filepath 下所有文件，包括子目录
    files = os.listdir(folderPath_)
    for _fileName in files:
        _fileOrFolderPath = os.path.join(folderPath_, _fileName)
        if os.path.isdir(_fileOrFolderPath):
            gci(_fileOrFolderPath, fileFilters_, filePathList_, False)  # 是文件夹
        else:
            _filePath = os.path.join(folderPath_, _fileOrFolderPath)  # 是文件
            _fileSuffix = utils.fileUtils.getUpperSuffix(_filePath)  # 当前的文件，后缀名（大写）
            if fileFilters_:  # 过滤的后缀列表
                if _filePath and not _fileSuffix == "" and (_fileSuffix in fileFilters_):
                    filePathList_.append(_filePath)
            else:  # 没有需要过滤的后缀列表，就全部记录下来
                filePathList_.append(_filePath)


# 将符合后缀类型的文件，构成 名称:路径 这样的键值对。
def getFilePathKeyValue(folderPath_: str, filters_: list, uesRelativePathAsKey_: bool = False):
    # 删
    return _keyValueDict


# 获取后缀名的文件列表
# fileList = folderUtils.getFilterFilesInPath(folderPath_,[".jpg"])
# 获取所有的文件列表
# fileList = folderUtils.getFilterFilesInPath(folderPath_)
def getFilterFilesInPath(folderPath_: str, filters_: list = None):
    _allFilePaths = []
    for root, dirs, files in os.walk(folderPath_):
        if filters_:  # 有过滤信息，就按照这个过滤
            _realFilePaths = [os.path.join(root, _file) for _file in files if utils.fileUtils.getSuffix(_file) in filters_]
        else:  # 没有过滤信息，就去全要
            _realFilePaths = [os.path.join(root, _file) for _file in files]
        _allFilePaths = _allFilePaths + _realFilePaths
    return _allFilePaths


# fileList = folderUtils.getFilterFilesInPathReg(folderPath_,[".*SkeletonData\.asset$"])
def getFilterFilesInPathReg(folderPath_: str, reStrList_: list = None):
    _allFilePaths = []
    for root, dirs, files in os.walk(folderPath_):
        if reStrList_:  # 有过滤信息，就按照这个过滤
            _realFilePaths = [os.path.join(root, _file) for _file in files if utils.strUtils.isStrInFilterRegList(reStrList_, _file)]
        else:  # 没有过滤信息，就去全要
            _realFilePaths = [os.path.join(root, _file) for _file in files]
        _allFilePaths = _allFilePaths + _realFilePaths
    return _allFilePaths


# 文件夹 folderPath_ 下的 oldName_ 文件更名为 newName_
def renameFileInFolder(folderPath_, oldName_, newName_):
    _oldPath = os.path.join(folderPath_, oldName_)
    _newPath = os.path.join(folderPath_, newName_)
    os.rename(_oldPath, _newPath)


# 文件目录是否有子文件夹
def isFolderHasSubFolder(folderPath_):
    if os.path.isdir(folderPath_):
        _filePathsInDir = os.listdir(folderPath_)
        for _fileName in _filePathsInDir:
            _filePath = os.path.join(folderPath_, _fileName)
            if os.path.isdir(_filePath):
                return True
    else:
        print("WARNING : folderUtils -> isFolderHasSubFolder : 不是一个文件夹 : " + folderPath_ + " ")
    return False


# 递归删除空文件夹
def deleteEmptyFolder(folderPath_: str, isMain_: bool = True):
    _filePathsInDir = os.listdir(folderPath_)
    if len(_filePathsInDir) == 0:
        os.removedirs(folderPath_)
    elif len(_filePathsInDir) == 1 and _filePathsInDir[0] == ".DS_Store":
        os.remove(os.path.join(folderPath_, _filePathsInDir[0]))
        os.removedirs(folderPath_)
    else:
        for _fileName in _filePathsInDir:
            _fileOrFolderPath = os.path.join(folderPath_, _fileName)
            if os.path.isdir(_fileOrFolderPath):
                deleteEmptyFolder(_fileOrFolderPath, False)


# 过滤后缀列表检测并大写
def suffixFiltersCheckAndUpper(filters_: list):
    if filters_ and len(filters_) > 0:
        # 遍历后缀抒写方式，必须是 ".后缀" 才合理
        for _idx in range(len(filters_)):
            if filters_[_idx] == "" or not filters_[_idx][0] == ".":
                raise Exception(
                    "当前后缀为 : \'" + filters_[_idx] + "\' ，后缀抒写必须是 .后缀 的格式"
                )
            # 将过滤后缀大写
            filters_[_idx] = filters_[_idx].upper()
    return filters_


# 获取文件列表
def getFileListInFolder(folder_: str, filters_: list = None):
    _filePathList = []
    # fix 最后一个字符为 /
    folder_ = utils.sysUtils.folderPathFixEnd(folder_)
    # 获取文件列表
    gci(folder_, filters_, _filePathList, True)
    return _filePathList


# 输出后缀种类，以及每种后缀的文件列表
def getSuffixInfoInFolder(folderPath_: str):
    folderPath_ = utils.sysUtils.folderPathFixEnd(folderPath_)
    _suffixInfoDict = {}
    _fileList = getFileListInFolder(folderPath_)  # 获取所有文件
    # 归类
    for _i in range(len(_fileList)):
        _filePath = _fileList[_i]
        _suffix = utils.fileUtils.getSuffix(_filePath)
        if not _suffix in _suffixInfoDict:
            _suffixInfoDict[_suffix] = {}
            _suffixInfoDict[_suffix]["count"] = 0
            _suffixInfoDict[_suffix]["suffix"] = _suffix
            _suffixInfoDict[_suffix]["fileList"] = []
        _suffixInfoDict[_suffix]["fileList"].append(_filePath)
        _suffixInfoDict[_suffix]["count"] = _suffixInfoDict[_suffix]["count"] + 1
    # 字典中的值存成列表
    _suffixInfoList = utils.listUtils.getDictValueAsList(_suffixInfoDict)
    # 列表按照 count 进行排序
    utils.listUtils.sortListOfDict(_suffixInfoList, "count", True)
    return _suffixInfoList


# 文件夹中查找字符串------------------------------------------------------------------------------------------------------------------------
# strList_ 要找的字符串的列表
# fileFilters_ 在什么类型的文件中找
# folder_ 目标文件夹
# needAll_ 结果集中的文件,是否必须包含全部 strList_ 的字符串.
def findStrInFolder(strList_: list, fileFilters_: list, folder_: str, needAll_: bool = False):
    _fileList = getFileListInFolder(folder_, fileFilters_)
    _resultList = []
    for _filePath in _fileList:  # 循环文件列表
        # 每一个File都重置成空
        _lineInfo = None
        for _str in strList_:  # 循环要匹配的字符串
            _lineStr = utils.fileUtils.fileHasString(_filePath, _str)
            if not _lineStr:  # 有匹配到的行
                if _lineInfo:
                    _lineInfo = _lineInfo
                else:
                    # 这个File里有才会成
                    _lineInfo = {}
                    _lineInfo["lineList"] = []
                    _lineInfo["filePath"] = _filePath
                _lineInfo["lineList"].append(_lineStr)

        if _lineInfo:  # 当前文件，是否有匹配消息
            if needAll_:  # 是否列表中的所有字符串都要满足
                _findCount = 0
                for _str in strList_:  # 传进来的每一个字符串,都满足
                    for _line in _lineInfo["lineList"]:
                        if _line.find(_str) >= 0:
                            _findCount += 1  # 找到当前的，就找下一个
                            break
                # 找到个数和要找的个一致，那么，这个文件就包含全部要找的内容
                if _findCount == len(strList_):
                    _resultList.append(_lineInfo)
            else:  # 不需要都满足，只要有匹配消息，就可以添加给返回值了
                _resultList.append(_lineInfo)
    return _resultList


# 满足 regStr_ 的名称（不带后缀的），转换成 targetFormat_ 的样式
# renameByReg("/Users/nobody/Downloads/book/", r"special \((\d+)\).gif", "special_{}.gif")
# special (12).gif -> special_12.gif
def renameByReg(folderPath_: str, regStr_: str, targetFormat_: str):
    _fileList = getFileNameListJustOneDepth(folderPath_)  # 获取所有文件(仅一层)
    for _i in range(len(_fileList)):
        _filePath = _fileList[_i]  # 文件路径
        _oldName = utils.fileUtils.fileName(_filePath)  # 文件名
        _formatReg = re.search(regStr_, _oldName)  # 匹配
        if _formatReg:  # 成立
            _matchStrList = []  # 匹配到的内容
            # SAMPLE - 正则，遍历所有匹配结果
            _length = len(_formatReg.groups())
            for _groupNum in range(0, _length):
                _matchStr = _formatReg.group(_groupNum + 1)
                _matchStrList.append(_matchStr)  # 内容存成列表
            _newName = targetFormat_.format(*_matchStrList)  # 列表写入给定格式
            renameFileInFolder(folderPath_, _oldName, _newName)  # 改名


# 备份文件夹，在当前文件夹所在的位置下，判断并创建副本
def folderBackUp(folderPath_: str):
    _folderParentPath = utils.sysUtils.getParentPath(folderPath_)  # 上层路径
    _backUpPath = os.path.join(_folderParentPath, utils.fileUtils.justName(folderPath_) + "_backUp")  # 搞一份备份
    if os.path.exists(_backUpPath):  # 有备份
        if not os.path.exists(folderPath_):  # 没有源，有可能删了。【代码执行错误的时候，会删除源，因为，源会变】
            shutil.copytree(_backUpPath, folderPath_)  # 将备份 同步给 源
            print("备份文件，拷贝回源路径")
        else:
            removeTree(folderPath_)  # 有源，这里的源，也是备份之后的，所以，可以用备份覆盖回去
            shutil.copytree(_backUpPath, folderPath_)
            utils.fileUtils.writeFileWithStr(folderPath_ + '/backup_created', 'backup end')  # 标记已经备份过了
            print("删除原路径，将备份还原回去")
        if not os.path.isfile(folderPath_ + '/backup_created'):  # 源里没有 创建备份的标示。
            removeTree(_backUpPath)  # 删除 原有备份
            shutil.copytree(folderPath_, _backUpPath)
            utils.fileUtils.writeFileWithStr(folderPath_ + '/backup_created', 'backup end')  # 标记已经备份过了
        else:
            print("已经创建过备份了")
    else:
        shutil.copytree(folderPath_, _backUpPath)  # 没备份文件 - 就备份一份
        utils.fileUtils.writeFileWithStr(folderPath_ + '/backup_created', 'backup end')  # 标记已经备份过了


# 文件夹中的每一个符合条件的文件，进行内容转换，重新写入另一个文件夹内
def convertFolderFiles(convertFunc_, srcFolderPath_: str, targetFolderPath_: str, filters_: list):
    _srcFile = utils.fileUtils.getPath(srcFolderPath_, "")
    _filePathList = getFileListInFolder(_srcFile, filters_)
    for _path in _filePathList:
        utils.fileUtils.convertFile(convertFunc_, _path, targetFolderPath_ + _path.split(srcFolderPath_).pop())


# 文件夹内的每一个符合条件的文件，执行方法
def doFunForeachFileInFolder(func_, srcFolderPath_: str, filters_: list):
    _csCodeFolder = utils.fileUtils.getPath(srcFolderPath_, "")
    _filePathList = getFileListInFolder(_csCodeFolder, filters_)
    for _path in _filePathList:
        func_(_path)


# 文件夹中，每一个符合条件的文件，移动到另一个文件夹中，保持现有文件递归结构【正则方式】
def moveFolderFilesReg(sourceFolderPath_: str, targetFolderPath_: str, reStrList_: list):
    _filePathList = getFilterFilesInPathReg(sourceFolderPath_, reStrList_)
    for _idx in range(len(_filePathList)):
        _shortPath = _filePathList[_idx].split(sourceFolderPath_)[1]
        _tarfilePath = targetFolderPath_ + _shortPath
        _sourcefilePath = sourceFolderPath_ + _shortPath
        print(str(_sourcefilePath) + ' -> ' + str(_tarfilePath))
        _targetFileLocalFolderPath = os.path.split(_tarfilePath)[0]
        makeSureDirIsExists(_targetFileLocalFolderPath)
        shutil.copy(_sourcefilePath, _tarfilePath)


# 重命名
# r'(.*?)([0-9]+)(.*)' 以数字结尾的正则
def renameNum(picFolderPath_, regStr_):
    _fileWithSuffixList = getFilterFilesInPath(picFolderPath_, [".jpg", ".jpeg"])
    _fileWithSuffixList.sort()

    if len(_fileWithSuffixList) == 0:
        raise Exception(picFolderPath_ + " : empty.")

    _pathToIntDict = {}
    _maxInt = 0
    for _i in range(len(_fileWithSuffixList)):
        _oldPath = _fileWithSuffixList[_i]
        _oldName = os.path.basename(_oldPath)
        _picNameReg = re.search(regStr_, _oldName)
        if _picNameReg:
            _picInt = utils.strUtils.convertToInt(_picNameReg.group(2))
            if _picInt > _maxInt:
                _maxInt = _picInt
            _pathToIntDict[_oldPath] = _picInt
        else:
            raise Exception(_oldName + " 正则匹配不到数字 : " + regStr_)

    _zeroCount = 1
    while _maxInt >= 10 ** _zeroCount:
        _zeroCount += 1

    for _path in _pathToIntDict:
        _oldName = os.path.basename(_path)
        _picNameReg = re.search(regStr_, _oldName)
        _newName = _picNameReg.group(1) + \
                   str(_pathToIntDict[_path]).rjust(_zeroCount, "0") + \
                   _picNameReg.group(3)
        renameFileInFolder(picFolderPath_, _oldName, _newName)


# 交换排序后相邻两个文件的名称
def switchNearByFileNames(picFolderPath_):
    _fileWithSuffixList = getFilterFilesInPath(picFolderPath_, [".jpg", ".jpeg"])
    _fileWithSuffixList.sort()
    # 交换相邻两个文件的名称
    for _i in range(len(_fileWithSuffixList)):
        if _i % 2 == 1:
            continue
        _currentName = os.path.basename(_fileWithSuffixList[_i])
        _targetName = os.path.basename(_fileWithSuffixList[_i + 1])
        _tempName = "xx.jpg"
        renameFileInFolder(picFolderPath_, _targetName, _tempName)
        renameFileInFolder(picFolderPath_, _currentName, _targetName)
        renameFileInFolder(picFolderPath_, _tempName, _currentName)


# 从 folderA_ 中 删除已经在 folderB_ 中存在的的文件，匹配条件为文件名
def removeAFilesInB(folderA_, folderB_, filters_):
    _filesInA = getFilterFilesInPath(folderA_, filters_)
    _filesInB = getFilterFilesInPath(folderB_, filters_)
    _filesNameInB = []
    for _i in range(len(_filesInB)):
        _targetPath = _filesInB[_i]
        _fileName = os.path.basename(_targetPath)
        _filesNameInB.append(_fileName)

    for _i in range(len(_filesInA)):
        _targetPath = _filesInA[_i]
        _fileName = os.path.basename(_targetPath)
        if _fileName in _filesNameInB:
            os.remove(_targetPath)


def removeTree(folderPath_):
    checkFolderDepth(folderPath_)
    shutil.rmtree(folderPath_)


def checkFolderDepth(fileOrFolderPath_: str):
    if os.path.exists(fileOrFolderPath_):
        # 判断是否正在删除根目录。。。
        if fileOrFolderPath_.index(os.sep) < 0:
            utils.printUtils.pError("ERROR : 别乱删" + fileOrFolderPath_)
            sys.exit(1)
        else:
            _deleteSplitLength = len(fileOrFolderPath_.split(os.sep))
            if _deleteSplitLength <= 5:
                # 一般本机的目录结构。为了不错误的删除了内容，进行了一次强制长度判断。太短的路径，不会进行删除
                # /盘符/子盘目录/自定义分类/ -- 移动硬盘的情况
                # /Users/用户/分类(Download、desktop)/自定义分类/ -- 本机目录的情况 <以这个为安全层级数，防止误删除>
                utils.printUtils.pError("ERROR : 路径有点儿短，别删错了 " + fileOrFolderPath_)
                sys.exit(1)


# 获得 指定类型的文件列表
def getAllFileBySuffix(folderPath_: str, targetSuffix_: str, finalList_: list = None):
    if finalList_ == None:
        finalList_ = []
    files = os.listdir(folderPath_)
    for _i in range(len(files)):
        _filePath = os.path.join(folderPath_, files[_i])
        if os.path.isdir(_filePath):
            _suffix = utils.fileUtils.getSuffix(_filePath)
            if _suffix == targetSuffix_:
                finalList_.append(_filePath)
            else:
                getAllFileBySuffix(_filePath, targetSuffix_, finalList_)
    return finalList_


def checkFolderExist(folderPath_: str):
    _splitList = os.path.abspath(folderPath_).split(os.sep)
    _currentFolderPath = ""
    _currentIdx = 0
    while _currentIdx < len(_splitList):
        _tempPath = _splitList[_currentIdx]
        _currentFolderPath = _currentFolderPath + _tempPath + os.sep
        if not os.path.exists(_currentFolderPath):
            print(f"ERROR : {folderPath_} - {_currentFolderPath} not exist.")
            return False
        _currentIdx = _currentIdx + 1
    return True


import os

if __name__ == "__main__":
    # 输出文件夹的结构
    folderPath = "/Users/nobody/Documents/develop/GitHub/puerTS/puerts-starter-kit/"
    showFileStructure(folderPath, "", ["Library", "Logs", "Temp", "node_modules", ".idea", ".vscode", ".git"])
    sys.exit(1)

    # 移除文件夹中的 meta 文件
    # removeFileByFilter(
    #     "/Users/nobody/Documents/develop/GitHub/Services/CS_Service/FGUI/",
    #     [".meta"]
    # )
    # sys.exit(1)

    # # 打印所有 bundle 的位置
    # _fileStructureDict = getFileStructure("/disk/XS/SLG/DEV/projects/cs/project_unity/", [".*\.bundle$"])
    # utils.printUtils.printPyObjAsKV("_fileStructureDict", _fileStructureDict)
    # sys.exit(1)

    # # 打印所有 CMake 的位置
    # _fileStructureDict = getFileStructure("/Users/nobody/Documents/develop/GitHub/Services/CSharp_Service/", [".*\.sln"])
    # utils.printUtils.printPyObjAsKV("_fileStructureDict", _fileStructureDict)
    # sys.exit(1)

    # psdFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(),"svn_repos/trunk")
    # showFileStructureReg(psdFolderPath, [".*\.psd$"], True)
    # sys.exit(1)

    # # 显示文件文件层级结构以及大小
    # psdFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(),"svn_repos/trunk/doc/art/UI/demo/pic/局内效果图")
    # showFileStructureReg(psdFolderPath, [".*\.json$"], True)
    # sys.exit(1)

    # # 输出某个文件夹内文件种类构成以及大小分别是多少。
    # _targetFolder = "/Volumes/Files/develop/loho/mini-game/miniclient/build/wechatgame/res/"
    # getFolderSizeInfo(_targetFolder)
    # sys.exit(1)

    # # 获取目标文件夹内，有哪些种类的文件
    # _targetFolder = os.path.join(Company_BB_Utils.getDebugProjectFolderPath(), "Assets/")
    # _suffixInfoList = getSuffixInfoInFolder("/Users/nobody/Downloads/VMBindPlugin/")
    # utils.listUtils.printDictList(_suffixInfoList, "{0} - {1}", ["suffix", "count"])
    # sys.exit(1)

    # # 查看文件夹下的cs文件都分布在那几个文件夹
    # _targetFolder = os.path.join(Company_BB_Utils.getDebugProjectFolderPath(), "Assets/")
    # _printList = getTypeLocateInfoInFolder(_targetFolder, ".unity3d", False)
    # utils.listUtils.printList(_printList)
    # sys.exit(1)

    # # 获取所有 .bundle
    # assetsPath = os.path.join(Company_BB_Utils.getDebugProjectFolderPath(), "Assets/")
    # _finalList = getAllFileBySuffix(assetsPath, ".bundle")
    # utils.listUtils.printList(_finalList)
    # sys.exit(1)

    # # 删除一层空白文件夹
    # deleteBlankFolderJustOneDepth("/Users/nobody/Documents/picUse/sizeFolder/")
    # sys.exit(1)

    # # 批量改名，只要名称满足条件不管后缀为何
    # renameByReg("/Users/nobody/Downloads/book/", r"special \((\d+)\).gif", "special_{}.gif")
    # sys.exit(1)

    # removeFileByFilter(os.path.join(Company_BB_Utils.getSLGProjectPath(),"project_ts/src"), [".js"])  # 再删除刚拷贝过的.pb文件
