#!/usr/bin/env python3
# Created by BB at 2023/2/15
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
import os
from utils import adbUtils
import sys


class BBLua_ExecuteOnAndroid(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(BBLua_ExecuteOnAndroid, self).create()

    def destroy(self):
        super(BBLua_ExecuteOnAndroid, self).destroy()

    # 新建文件将内容写入，然后打开文本框。执行脚本，之后在手机上将文本框内容当做lua执行
    def executeLua(self, fileName_):
        # 删

    # 结果文件的路径是固定的
    def getExecuteLuaResult(self):
        _resultFileName = "luaExecuteResult"  # 【不要改】执行脚本的日志名称
        _exeLuaResultFilePath = os.path.join(
            os.path.join(adbUtils.getStorageRoot(), "Android/data/{}/files/Log/"),
            _resultFileName
        )
        _packageName = adbUtils.getCurrentRunningAppPackageName()
        if _packageName == None:
            sys.exit(1)
        _exeLuaResultFilePath = _exeLuaResultFilePath.format(_packageName)
        adbUtils.pullFromSD(_exeLuaResultFilePath, os.path.join(self.subResPath, _resultFileName))


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    # 要上传执行的脚本名称，脚本在子服务的资源文件夹中
    _subSvr.executeLua("RenderQuality")
    # 获取 执行结果
    # _svr.getExecuteLuaResult()
