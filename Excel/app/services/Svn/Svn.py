#!/usr/bin/env python3
import os
from typing import List
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import cmdUtils
from utils import printUtils
from utils import listUtils
from utils import pyUtils
from utils import folderUtils
import sys
import re

'''
以下是 SVN 文件可能的状态：

- `A`：Added，表示文件或目录在提交前是新增的。
- `C`：Conflict，表示文件或目录的合并发生冲突。
- `D`：Deleted，表示文件或目录在提交前被删除了。
- `I`：Ignored，表示文件或目录被忽略。
- `M`：Modified，表示文件或目录在提交前被修改了。
- `R`：Replaced，表示文件或目录在提交前被替换了。
- `X`：External，表示当前目录是来自外部源的外部指针。
- `?`：Unversioned，表示文件或目录未进行版本管理。
- `!`：Missing，表示文件或目录已经被标记删除。

可以参考 SVN 官方文档了解各状态的含义。
'''
_statusReg = r'^([ACDIMRX?!])\s+([^\s]+)$'


class Svn(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(Svn, self).create()

    def destroy(self):
        super(Svn, self).destroy()

    # 检验状态是否合理
    def checkStatus(self, statusChar_: str):
        if 'A' == statusChar_ or 'C' == statusChar_ or 'D' == statusChar_ or 'I' == statusChar_ or 'M' == statusChar_ or 'R' == statusChar_ or 'X' == statusChar_ or '?' == statusChar_ or '!' == statusChar_:
            return True
        else:
            print(statusChar_ + " 类型，未定义")
            sys.exit(1)

    def fileListToStr(self, filePathList_: list):
        _filePathStr = ""
        for _idx in range(len(filePathList_)):
            _filePathStr += filePathList_[_idx] + " "
        return _filePathStr

    def checkFileListExist(self, svnProjectFolderPath_: str, filePathList_: list):
        for _i in range(len(filePathList_)):
            _filePath = os.path.join(svnProjectFolderPath_, filePathList_[_i])
            if not os.path.exists(_filePath):
                self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'{_filePath} 在 {svnProjectFolderPath_} 中不存在')

    # 获取给定文件列表的状态
    def svnStatusFileList(self, svnProjectFolderPath_: str, relativeFilePathList_: list):
        if not isinstance(relativeFilePathList_, list):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'relativeFilePathList_ 不是列表')
        self.checkFileListExist(svnProjectFolderPath_, relativeFilePathList_)  # 校验是否存在
        if relativeFilePathList_ is None or len(relativeFilePathList_) == 0:
            return []
        _filePathStr = self.fileListToStr(relativeFilePathList_)
        _cmd = f'svn status {_filePathStr}'  # 状态罗列
        _statusList = cmdUtils.doStrAsCmdAndGetPipeline(_cmd, svnProjectFolderPath_)
        return _statusList

    # 从状态输出中，找出满足条件的状态
    def getStatusMatchFileList(self, targetStatus_: str, statusList_: str):
        if self.checkStatus(targetStatus_):
            _fileList = []
            for _i in range(len(statusList_)):
                _status = statusList_[_i]
                _matches = re.findall(_statusReg, _status)
                for _status, _filePath in _matches:
                    self.checkStatus(_status)  # 检验
                    if _status == targetStatus_:
                        _fileList.append(_filePath)
            return _fileList
        return []

    # 尝试添加文件
    def svnAddFileList(self, svnProjectFolderPath_: str, relativeFilePathList_: List[str]):
        if not isinstance(relativeFilePathList_, list):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'relativeFilePathList_ 不是列表')
        _statusList = self.svnStatusFileList(svnProjectFolderPath_, relativeFilePathList_)
        _matchFilePathList = self.getStatusMatchFileList("?", _statusList)  # 找出未在版本管理里的
        if len(_matchFilePathList) > 0:
            _filePathStr = self.fileListToStr(_matchFilePathList)
            _cmd = f'svn add {_filePathStr}'  # 将其添加
            cmdUtils.doStrAsCmd(_cmd, svnProjectFolderPath_)

    # 尝试回滚冲突文件
    def svnRevertConflictFileList(self, svnProjectFolderPath_: str, relativeFilePathList_: List[str]):
        if not isinstance(relativeFilePathList_, list):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'relativeFilePathList_ 不是列表')
        _statusList = self.svnStatusFileList(svnProjectFolderPath_, relativeFilePathList_)
        _conflictFilePathList = self.getStatusMatchFileList("C", _statusList)  # 冲突的部分找出来
        if len(_conflictFilePathList) > 0:
            _filePathStr = self.fileListToStr(_conflictFilePathList)
            _cmd = f'svn resolve --accept theirs-full {_filePathStr}'  # 使用远端解决冲突，放弃本地变更
            cmdUtils.doStrAsCmd(_cmd, svnProjectFolderPath_)

    # 尝试添加文件夹
    def svnAddFolderList(self, svnProjectFolderPath_: str, relativeFolderPathList_: List[str]):
        if not isinstance(relativeFolderPathList_, list):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'relativeFolderPathList_ 不是列表')
        # 一个个文件夹提交
        for _idx in range(len(relativeFolderPathList_)):
            _relativePathList = []
            _relativeFolderPath = relativeFolderPathList_[_idx]  # 相对路径
            _folderPath = os.path.join(svnProjectFolderPath_, _relativeFolderPath)  # 实际路径
            if os.path.exists(_folderPath):
                # 添加文件夹，对于 svn 文件夹也是一个路径
                self.svnAddFileList(svnProjectFolderPath_, [_relativeFolderPath])
                # 添加文件夹下的文件
                _fileList = folderUtils.getFilterFilesInPath(_folderPath)  # 文件列表
                for _idxLoop in range(len(_fileList)):
                    _filePath = _fileList[_idxLoop]
                    _relativePath = os.path.relpath(_filePath, svnProjectFolderPath_)  # 转换回 相对路径
                    _relativePathList.append(_relativePath)
                self.svnAddFileList(svnProjectFolderPath_, _relativePathList)

    # 将指定文件提交
    def svnCommitFileList(self, svnProjectFolderPath_: str, relativeFilePathList_: list, commitCommon_: str):
        if not isinstance(relativeFilePathList_, list):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'relativeFilePathList_ 不是列表')
        if os.linesep in commitCommon_:
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), " commitCommon_ 不能存在换行符")
            sys.exit(1)
        self.svnAddFileList(svnProjectFolderPath_, relativeFilePathList_)  # 将没添加的先添加
        _statusList = self.svnStatusFileList(svnProjectFolderPath_, relativeFilePathList_)
        _addFileList = self.getStatusMatchFileList("A", _statusList)  # 添加的
        _modifyFileList = self.getStatusMatchFileList("M", _statusList)  # 修改的
        _commitFileList = _addFileList.extend(_modifyFileList)  # 合并成将要提交的
        if _commitFileList is not None and len(_commitFileList) > 0:
            _filePathStr = self.fileListToStr(_commitFileList)
            _cmd = f'svn commit -m "{commitCommon_}" {_filePathStr}'  # 将其添加
            cmdUtils.doStrAsCmd(_cmd, svnProjectFolderPath_)
        else:
            print("没有可提交项目")

    # 更新指定文件
    def svnUpdateFileList(self, svnProjectFolderPath_: str, relativeFilePathList_: list):
        if not isinstance(relativeFilePathList_, list):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'relativeFilePathList_ 不是列表')
        self.checkFileListExist(svnProjectFolderPath_, relativeFilePathList_)  # 校验是否存在
        _filePathStr = self.fileListToStr(relativeFilePathList_)  # 拼接成文件列表字符串
        _cmd = f'svn update {_filePathStr}'  # 更新一下
        cmdUtils.doStrAsCmd(_cmd, svnProjectFolderPath_)

    # 更新指定多个文件夹
    def svnUpdateFolderList(self, svnProjectFolderPath_: str, relativeFolderPathList_: list):
        if not isinstance(relativeFolderPathList_, list):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'relativeFolderPathList_ 不是列表')
        for _i in range(len(relativeFolderPathList_)):
            _relativeFolderPath = relativeFolderPathList_[_i]
            _folderPath = os.path.join(svnProjectFolderPath_, _relativeFolderPath)
            if os.path.exists(_folderPath):
                if os.path.isdir(_folderPath):
                    _cmd = f'svn update --depth infinity {_relativeFolderPath}'
                    cmdUtils.doStrAsCmd(_cmd, svnProjectFolderPath_)
                else:
                    self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'{_folderPath} 不是文件夹')
            else:
                self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'{_folderPath} 不存在')


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
'''
from Excel.app.services.Svn import Svn
_svr : Svn = pyServiceUtils.getSvrByName("Excel", "Svn")
'''
