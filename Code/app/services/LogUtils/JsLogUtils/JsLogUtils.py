#!/usr/bin/env python3
# Created by nobody at 2024/1/23
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import folderUtils
from utils import fileUtils
from utils import printUtils
from utils import cmdUtils
import os
import re
from pathlib import Path


class JsLogUtils(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(JsLogUtils, self).create()

    def destroy(self):
        super(JsLogUtils, self).destroy()

    # 获取相对路径，来生成 require
    def getRelativePath(self, logUtilsPath_: str, jsCodePath_: str):
        logUtilsPath_ = os.path.realpath(logUtilsPath_)
        jsCodePath_ = os.path.realpath(jsCodePath_)
        jsCodePath_ = Path(jsCodePath_)
        relativePath = os.path.relpath(logUtilsPath_, jsCodePath_.parent)
        return relativePath.split('.js')[0]

    def analyseJsFolder(self, distFolderPath_: str, jsRelativeFolderPath_: str, logUtilsRelativePath_: str):
        # 确保 ts 监控关闭，免得 覆盖掉刚修改过的js代码
        cmdUtils.checkAndKillCmdList([
            "tsc --watch --project tsconfig.json", "tsc-watch"
        ])
        # 确保日志存在
        _logUtilsPath = os.path.join(distFolderPath_, logUtilsRelativePath_)
        if not os.path.exists(_logUtilsPath):
            printUtils.pWarn(f"copy LogUtils.js to {_logUtilsPath}")
            folderUtils.makeSureDirIsExists(os.path.split(_logUtilsPath)[0])  # 确保 目录存在
            fileUtils.copyTo(os.path.join(self.subResPath, "support/LogUtils.js"), _logUtilsPath)  # 拷贝文件
        # 获得 js 文件
        _filePathDict = folderUtils.getFilePathKeyValue(
            os.path.join(distFolderPath_, jsRelativeFolderPath_),
            [".js"],
            True
        )
        # 挨个 添加 日志
        for _, _jsCodePath in _filePathDict.items():  # 相对路径
            _logUtilsRelativeToJsCodePath = self.getRelativePath(_logUtilsPath, _jsCodePath)
            self.analyseJSFile(_jsCodePath, _logUtilsRelativeToJsCodePath)

    # 写入日志。日志类的相对路径
    def analyseJSFile(self, jsFilePath_: str, logUtilsRelativeToJsCodePath_: str):
        # 删


if __name__ == '__main__':
    _subSvr_JsLogUtils: JsLogUtils = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr_JsLogUtils.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    sys.exit(1)
    from utils.CompanyUtil import Company_BB_Utils

    _distPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/dist/")
    _jsFolderRelativePath = "Game/Module/"
    # _jsFolderRelativePath = "Game/Module/Guide/"
    _logUtilRelativePath = "Framework/ABDebug/LogUtils.js"
    _subSvr_JsLogUtils.analyseJsFolder(_distPath, _jsFolderRelativePath, _logUtilRelativePath)

    # _relativePath = _subSvr.getRelativePath(
    #     os.path.join(_distPath, _logUtilRelativePath),
    #     os.path.join(Company_BB_Utils.getSLGProjectPath(),"project_ts/dist/Game/Module/Guide/GuideMgr.js")
    # )
    #
    # print('_relativePath = ' + str(_relativePath))
