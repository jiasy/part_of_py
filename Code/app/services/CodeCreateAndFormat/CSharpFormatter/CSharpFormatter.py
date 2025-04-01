#!/usr/bin/env python3
# Created by nobody at 2023/12/23
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import sysUtils
from utils import cmdUtils
from utils import folderUtils
from utils import fileUtils
from utils import fileContentOperateUtils
import os
import sys


class CSharpFormatter(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(CSharpFormatter, self).create()

    def destroy(self):
        super(CSharpFormatter, self).destroy()

    # 格式化工具
    def checkInstallFormat(self):
        sysUtils.dotnetCheckThenInstall("dotnet-format")

    # 格式化工程代码，只支持工程整个格式化
    def formatCsProject(self, projectFolder_: str):
        if not os.path.exists(projectFolder_):
            print(f"ERROR : {projectFolder_} not exist")
            sys.exit(1)
        # 判断工程文件是否存在
        _slnFileName = folderUtils.getFileNameListJustOneDepth(projectFolder_, ['.sln'])[0]
        _slnFile = os.path.join(projectFolder_, _slnFileName)
        if not os.path.exists(_slnFile):
            print(f"ERROR : {_slnFile} not exist")
            sys.exit(1)
        # 拷贝 格式化配置
        _editorconfigPath = os.path.join(self.subResPath, "support", ".editorconfig")
        if not os.path.exists(_editorconfigPath):
            print(f"ERROR : .editorconfig 不存在")
            sys.exit(1)
        fileUtils.copyTo(_editorconfigPath, os.path.join(projectFolder_, ".editorconfig"))
        # 执行工程格式化
        _cmdStr = f'dotnet format ./{_slnFileName}'
        cmdUtils.doStrAsCmd(_cmdStr, projectFolder_)
        # 多行空白行变一行
        _csFileList = folderUtils.getFileListInFolder(projectFolder_, ['.cs'])
        for _i in range(len(_csFileList)):
            fileContentOperateUtils.removeMultipleBlankLine(_csFileList[_i])


if __name__ == '__main__':
    _subSvr_CSharpFormatter: CSharpFormatter = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr_CSharpFormatter.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    # # 安装格式化工具
    # _subSvr_CSharpFormatter.checkInstallFormat()

    from Proto.app.services.ProtoToClass.ProtoToCsClass import ProtoToCsClass

    _protoToCsClass: ProtoToCsClass = pyServiceUtils.getSubSvrByName("Proto", "ProtoToClass", "ProtoToCsClass")
    _excelConfigProjectFolder = os.path.join(_protoToCsClass.subResPath, "ExcelConfig")
    if not os.path.exists(_excelConfigProjectFolder):
        print(f"ERROR : {_excelConfigProjectFolder} not exist")
        sys.exit(1)
    _subSvr_CSharpFormatter.formatCsProject(_excelConfigProjectFolder)
