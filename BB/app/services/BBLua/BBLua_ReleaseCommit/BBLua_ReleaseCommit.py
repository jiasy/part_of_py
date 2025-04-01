#!/usr/bin/env python3
# Created by BB at 2023/3/29
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import fileCopyUtils
from utils import folderUtils
from utils import fileUtils
from utils import listUtils
from utils import pyUtils
import os
from Excel.app.services.Svn import Svn
from enum import Enum


# 库类型
class PathType(Enum):
    NONE = 0
    DEV = 1  # 开发
    REL = 2  # 发布
    TW_DEV = 3  # 开发 - 台湾
    TW_REL = 4  # 发布 - 台湾


class BBLua_ReleaseCommit(BaseInService):
    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.sourceCompareAppPath = "/Applications/Beyond\ Compare.app/Contents/MacOS/bcomp"
        # 四个库的路径
        self.releasePath = "/Volumes/XM/develop/XM/XA/release/release/"
        self.twReleasePath = "/Volumes/XM/develop/XM/XA/twRelease/release/release/"
        self.developPath = "/Volumes/XM/develop/XM/XM/"
        self.twDevelopPath = "/Volumes/XM/develop/XM/XA/TWDevelop/"
        # 关键路径的相对位置
        self.data_path = "Assets/Dev/Lua/Game/Module/data/"
        self.service_path = "Assets/Dev/Lua/Game/Module/service/"
        self.logic_path = "Assets/Dev/Lua/Game/Module/logic/"
        self.ui_path = "Assets/Dev/Lua/ui/page/"
        # 开发库中lua脚本的位置
        self.develop_lua_path = os.path.join(self.developPath, "Assets/Dev/XX/")
        self.svnTool: Svn = pyServiceUtils.getSvrByName("Excel", "Svn")

    def create(self):
        super(BBLua_ReleaseCommit, self).create()

    def destroy(self):
        super(BBLua_ReleaseCommit, self).destroy()

    def getRealPath(self, pathType_: PathType):
        if pathType_ == PathType.REL:
            return self.releasePath
        if pathType_ == PathType.TW_DEV:
            return self.twDevelopPath
        if pathType_ == PathType.TW_REL:
            return self.twReleasePath
        if pathType_ == PathType.DEV:
            return self.developPath
        sys.exit(1)

    # 拷贝文件
    def copyRelativeFile(self, relativePath_: str, pathType_: PathType, fromPathType_: PathType = PathType.DEV):
        _realTargetPath = self.getRealPath(pathType_)
        _fromPath = self.getRealPath(fromPathType_)
        _prefix = '                    '
        if pathType_ == PathType.TW_REL:
            _prefix = '                              '
        if pathType_ == PathType.TW_DEV:
            _prefix = '              '
        _srcPath = os.path.join(_fromPath, relativePath_)
        _tarPath = os.path.join(_realTargetPath, relativePath_)
        fileCopyUtils.copyFile(_srcPath, _tarPath)
        # 拷贝 meta
        if os.path.exists(_srcPath + ".meta"):
            fileCopyUtils.copyFile(_srcPath + ".meta", _tarPath + ".meta")
            print(_prefix + str(_srcPath))
            print('     -> ' + str(_tarPath))

    def printCmdRelativePath(self, relativePath_: str, pathType_: PathType, fromPathType_: PathType = PathType.DEV):
        _realTargetPath = self.getRealPath(pathType_)
        _fromPath = self.getRealPath(fromPathType_)
        # 自动提交的不用比较
        if "Assets/Dev/Lua/AutoGen/luaIde/UIPageConfig.gen.lua" == relativePath_:
            return
        _developFilePath = os.path.join(_fromPath, relativePath_)
        _releaseFilePath = os.path.join(_realTargetPath, relativePath_)
        self.printCmd(_developFilePath, _releaseFilePath)

    def printCmd(self, developFilePath_, releaseFilePath_):
        _cmdStr = "{app} {develop} {release}".format(app=self.sourceCompareAppPath, develop=developFilePath_, release=releaseFilePath_)
        print(str(_cmdStr))

    # 那些文件包含指定字符串
    def getFilePathContainsStr(self, strList_: list):
        # 创建 字符串 和 文件列表 的 关系结构
        _strToPathListDict = dict()
        for _idx in range(len(strList_)):
            _strToPathListDict[strList_[_idx]] = list()
        # 遍历文件，将 字符串 和 文件列表 的关系写入结构
        _luaFilePathList = folderUtils.getFileListInFolder(self.develop_lua_path, [".lua"])
        for _idx in range(len(_luaFilePathList)):
            _luaFilePath = _luaFilePathList[_idx]
            for _idxLoop in range(len(strList_)):
                _str = strList_[_idxLoop]
                if fileUtils.fileHasString(_luaFilePath, _str):
                    _strToPathListDict[_str].append(_luaFilePath.split(self.developPath)[1])
        return _strToPathListDict

    # 模糊查询
    def getRelativePathByFileNameList(self, partOfNameList_: str, needPrint_: bool = False):
        _pathAllList = list()  # 总表
        for _idx in range(len(partOfNameList_)):
            self.getRelativePathByFileName(partOfNameList_[_idx], needPrint_, _pathAllList)
        return _pathAllList

    # 模糊查询一部分
    def getRelativePathByFileName(self, partOfName_: str, needPrint_: bool = False, pathAllList_: list = None):
        if pathAllList_ is None:
            pathAllList_ = list()
        # 遍历文件，将 字符串 和 文件列表 的关系写入结构
        _luaFilePathList = folderUtils.getFileListInFolder(self.develop_lua_path, [".lua"])
        for _idx in range(len(_luaFilePathList)):
            _luaFilePath = _luaFilePathList[_idx]
            if partOfName_ in _luaFilePath:
                if not self.developPath in _luaFilePath:
                    self.raiseError(pyUtils.getCurrentRunningFunctionName(), " 不在 " + self.develop_lua_path + " 中\n" + _luaFilePath)
                _relativePath = _luaFilePath.split(self.developPath)[1]
                if needPrint_:
                    print(_relativePath)
                if not _luaFilePath in pathAllList_:  # 记录到总表中
                    pathAllList_.append(_relativePath)
        return pathAllList_

    # 打印 字符串 在文件中位置
    def printFilePathAndStrInfo(self, strList_: list, needPrint_: bool = False):
        _strToPathListDict = self.getFilePathContainsStr(strList_)
        _pathAllList = list()  # 总表
        for _key in _strToPathListDict:
            _filePathList = _strToPathListDict[_key]
            # 打印 子表
            if needPrint_:
                listUtils.printList(_filePathList, _key + " ---------------------------------------------- \n", "    ")
            for _idx in range(len(_filePathList)):
                _filePath = _filePathList[_idx]
                if not _filePath in _pathAllList:  # 记录到总表中
                    _pathAllList.append(_filePath)
        # 打印总表
        if needPrint_:
            listUtils.printList(_pathAllList, " ALL ===================================================== \n", "    ")
        return _pathAllList

    # 将指定文件复制出另外几份，并将其中指定内容按照键值对替换
    def duplicateFile(self, srcRelativePath_: str, replaceKV_: dict, targetRelativePath_: str):
        _srcFilePath = os.path.join(self.develop_lua_path, srcRelativePath_)
        _tarFilePath = os.path.join(self.develop_lua_path, targetRelativePath_)
        _content = fileUtils.readFromFile(_srcFilePath)
        for _key in replaceKV_:
            _value = replaceKV_[_key]
            _content = _content.replace(_key, _value)
        fileUtils.writeFileWithStr(_tarFilePath, _content)

    # 大多数公用文件
    def getCommonFileList(self):
        return [
            # 删
        ]

    # 打印 Source Compare 所需比较的文件
    def printCommonBeyondCompareCMD(self, pathType_: PathType):
        _fileList = self.getCommonFileList()
        # 打印
        for _idx in range(len(_fileList)):
            self.printCmdRelativePath(_fileList[_idx], pathType_)

    # 共同文件的更新
    def commonSvnUpdateAll(self):
        _fileList = self.getCommonFileList()
        self.svnTool.svnUpdateFileList(self.twReleasePath, _fileList)  # 台湾 release
        self.svnTool.svnUpdateFileList(self.twDevelopPath, _fileList)  # 台湾 develop
        self.svnTool.svnUpdateFileList(self.releasePath, _fileList)  # release
        self.svnTool.svnUpdateFileList(self.developPath, _fileList)  # develop

    # 更新所有的Asset
    def assetSvnUpdateAll(self):
        _fileList = self.getCommonFileList()
        _folderPathList = ["Assets"]
        self.svnTool.svnUpdateFolderList(self.twReleasePath, _folderPathList)  # 台湾 release
        self.svnTool.svnUpdateFolderList(self.twDevelopPath, _folderPathList)  # 台湾 develop
        self.svnTool.svnUpdateFolderList(self.releasePath, _folderPathList)  # release
        self.svnTool.svnUpdateFolderList(self.developPath, _folderPathList)  # develop

    # 拷贝模块列表
    def moveListToRelease(self, moduleNameList_: list, pathType_: PathType, fromPathType_: PathType = PathType.DEV):
        for _idx in range(len(moduleNameList_)):
            self.moveToRelease(moduleNameList_[_idx], pathType_, fromPathType_)

    # 指定模块 add 到 svn 管理
    def moduleSvnAdd(self, moduleName_: str, pathType_: PathType):
        _realTargetPath = self.getRealPath(pathType_)  # 获取当前工程目录
        # 相对路径 folder
        _relative_ui_folder_path = os.path.join(self.ui_path, "{moduleName}").format(moduleName=moduleName_)
        _relative_data_folder_path = os.path.join(self.data_path, "{moduleName}").format(moduleName=moduleName_)
        _relative_service_folder_path = os.path.join(self.service_path, "{moduleName}").format(moduleName=moduleName_)
        _relative_logic_folder_path = os.path.join(self.logic_path, "{moduleName}").format(moduleName=moduleName_)
        # 相对路径 meta
        _relative_ui_meta_path = f'{_relative_ui_folder_path}.meta'
        _relative_data_meta_path = f'{_relative_data_folder_path}.meta'
        _relative_service_meta_path = f'{_relative_service_folder_path}.meta'
        _relative_logic_meta_path = f'{_relative_logic_folder_path}.meta'
        # 添加 meta 文件
        _protoStructList = [_relative_ui_meta_path, _relative_data_meta_path, _relative_service_meta_path, _relative_logic_meta_path]
        self.svnTool.svnAddFileList(_realTargetPath, _protoStructList)
        # 添加 文件夹内容
        _relativeFolderList = [_relative_ui_folder_path, _relative_data_folder_path, _relative_service_folder_path, _relative_logic_folder_path]
        self.svnTool.svnAddFolderList(_realTargetPath, _relativeFolderList)

    # 拷贝模块
    def moveToRelease(self, moduleName_: str, pathType_: PathType, fromPathType_: PathType = PathType.DEV):
        if moduleName_ is None:
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), "模块名未定义")
            return
        _realTargetPath = self.getRealPath(pathType_)
        _fromPath = self.getRealPath(fromPathType_)
        # 直接拷贝到Release的部分
        folderUtils.makeSureDirIsExists(os.path.join(_realTargetPath, self.data_path, "{moduleName}").format(moduleName=moduleName_))
        folderUtils.makeSureDirIsExists(os.path.join(_realTargetPath, self.service_path, "{moduleName}").format(moduleName=moduleName_))
        folderUtils.makeSureDirIsExists(os.path.join(_realTargetPath, self.logic_path, "{moduleName}").format(moduleName=moduleName_))
        folderUtils.makeSureDirIsExists(os.path.join(_realTargetPath, self.ui_path, "{moduleName}").format(moduleName=moduleName_))
        self.copyRelativeFile(os.path.join(self.ui_path, "{moduleName}.meta".format(moduleName=moduleName_)), pathType_, fromPathType_)
        self.copyRelativeFile(os.path.join(self.data_path, "{moduleName}.meta".format(moduleName=moduleName_)), pathType_, fromPathType_)
        self.copyRelativeFile(os.path.join(self.service_path, "{moduleName}.meta".format(moduleName=moduleName_)), pathType_, fromPathType_)
        self.copyRelativeFile(os.path.join(self.logic_path, "{moduleName}.meta".format(moduleName=moduleName_)), pathType_, fromPathType_)
        self.copyRelativeFile("Assets/Dev/Lua/Game/Module/logic/SevenDaysUnionAct/PageLogicDataServiceUtils.lua", pathType_, fromPathType_)
        _filters = None

        # 文件夹内全部拷贝过去
        fileCopyUtils.copyFilesInDir(
            os.path.join(_fromPath, self.ui_path, "{moduleName}").format(moduleName=moduleName_),
            os.path.join(_realTargetPath, self.ui_path, "{moduleName}").format(moduleName=moduleName_),
            True, _filters
        )
        fileCopyUtils.copyFilesInDir(
            os.path.join(_fromPath, self.data_path, "{moduleName}").format(moduleName=moduleName_),
            os.path.join(_realTargetPath, self.data_path, "{moduleName}").format(moduleName=moduleName_),
            True, _filters
        )
        fileCopyUtils.copyFilesInDir(
            os.path.join(_fromPath, self.service_path, "{moduleName}").format(moduleName=moduleName_),
            os.path.join(_realTargetPath, self.service_path, "{moduleName}").format(moduleName=moduleName_),
            True, _filters
        )
        fileCopyUtils.copyFilesInDir(
            os.path.join(_fromPath, self.logic_path, "{moduleName}").format(moduleName=moduleName_),
            os.path.join(_realTargetPath, self.logic_path, "{moduleName}").format(moduleName=moduleName_),
            True, _filters
        )
        # 移除掉 infos 内容
        folderUtils.removeTree(os.path.join(_realTargetPath, self.service_path, "{moduleName}".format(moduleName=moduleName_), "infos"))


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    # _subSvr.printCommonBeyondCompareCMD()
    # _subSvr.moveToRelease("DailyRecharge")

    # # 根据文件名的一部分，获取文件的相对路径
    # _partOfNameList = [
    #     "DailyRechargeCell",
    # ]
    # _fileList = _subSvr.getRelativePathByFileNameList(_partOfNameList, False)
    # # 打印
    # for _idx in range(len(_fileList)):
    #     _subSvr.printCmdRelativePath(_fileList[_idx])
