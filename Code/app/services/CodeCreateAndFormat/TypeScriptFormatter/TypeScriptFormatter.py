#!/usr/bin/env python3
# Created by nobody at 2023/12/20
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import cmdUtils
from utils import printUtils
from utils import folderUtils
from utils import fileUtils
import os


# 格式化工具，用于代码生成后的格式化工作
class TypeScriptFormatter(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(TypeScriptFormatter, self).create()

    def destroy(self):
        super(TypeScriptFormatter, self).destroy()

    # 检测并尝试安装 prettier
    def checkInstallPrettier(self):
        cmdUtils.brewCheckThenInstall("prettier")

    # 格式化 文本
    def formatTsStr(self, tsStr_: str):
        _tempFolder = os.path.join(self.subResPath, "temp")
        folderUtils.makeSureDirIsExists(_tempFolder)
        _tempTsFile = os.path.join(_tempFolder, "formatTsStr.ts")
        fileUtils.writeFileWithStr(_tempTsFile, tsStr_)
        self.formatTsFile(_tempTsFile)
        return fileUtils.readFromFile(_tempTsFile)

    # 格式化 文件
    def formatTsFile(self, tsFilePath_: str):
        if not os.path.exists(tsFilePath_):
            print(f"ERROR : {tsFilePath_} not exist")
            sys.exit(1)
        _prettierConfigPath = os.path.join(self.subResPath, "support", "custom-prettier-config.js")
        if not os.path.exists(_prettierConfigPath):
            printUtils.pError("ERROR : 没找到配置")
            sys.exit(1)
        _folderPath = os.path.split(tsFilePath_)[0]
        _cmdStr = f"prettier --config {_prettierConfigPath} --write '{tsFilePath_}'"
        cmdUtils.doStrAsCmd(_cmdStr, _folderPath)

    def formatTsFolder(self, tsFolderPath_: str):
        if not os.path.exists(tsFolderPath_):
            print(f"ERROR : {tsFolderPath_} not exist")
            sys.exit(1)
        _tsFileList = folderUtils.getFileListInFolder(tsFolderPath_, ['.ts'])
        for _i in range(len(_tsFileList)):
            self.formatTsFile(_tsFileList[_i])


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr: TypeScriptFormatter = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    from utils.CompanyUtil import Company_BB_Utils

    _tsFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/")  # TS 工程路径

    _formatTargetTS = os.path.join(_tsFolder, "src/Debug/HeroBagDebug.ts")

    _subSvr.formatTsFile(_formatTargetTS)

    # _codeStr = _subSvr.formatTsStr("")
    # print(_codeStr)
