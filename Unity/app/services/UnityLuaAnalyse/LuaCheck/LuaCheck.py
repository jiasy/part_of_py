#!/usr/bin/env python3
# Created by nobody at 2023/4/23
import os.path

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import pyUtils
from utils import cmdUtils
from utils import fileUtils


class LuaCheck(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(LuaCheck, self).create()

    def destroy(self):
        super(LuaCheck, self).destroy()

    def checkLuaFolder(self, luaFolderPath_: str, logFilePath_: str):
        if not os.path.exists(luaFolderPath_):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'{luaFolderPath_} 不存在')
        _cmd = "luacheck ./"
        _lines = cmdUtils.doStrAsCmdAndGetPipeline(_cmd, luaFolderPath_)
        fileUtils.writeFileWithStr(logFilePath_, "\n".join(_lines))


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    _luaFolderPath = "/disk/XS/wp_client/Assets/Dev/Lua/"
    _logFilePath = "/Users/nobody/Downloads/rar/Log"
    # _subSvr.checkLuaFolder(_luaFolderPath, _logFilePath)
    _strList = [
        "accessing undefined variable",  # 为定义的变量，一般是 C# 导出的
        "line is too long",  # 一行太长了
        "line contains trailing whitespace",  # 行结尾有空格
        "trailing whitespace in a comment",  # 注释里有空格啥的
        "line contains only whitespace",  # 只有空白的行

        "AutoGen/",  # 自动生成的
        "ConfigScript/",  # 配置
        "DataCenter/",  # 我的
        "net/protobuflua/",  # pb 生成
    ]
    _cmd = f"grep -vE '{'|'.join(_strList)}' {_logFilePath} > {_logFilePath}_Fix"
    cmdUtils.doStrAsCmdAndGetPipeline(_cmd, os.getcwd())

    # # 字符串替换
    # _oldStrList = []
    # _newStrList = []
    # for _idx in range(len(_oldStrList)):
    #     _oldStr = _oldStrList[_idx]
    #     _newStr = _newStrList[_idx]
    #     _cmd = f'sed -i \'s/{_oldStr}/{_newStr}/g\' {_logFilePath}_Fix'
    #     cmdUtils.doStrAsCmdAndGetPipeline(_cmd, os.getcwd())
