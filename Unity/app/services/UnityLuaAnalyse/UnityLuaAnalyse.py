#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from Unity.app.services.UnityLuaAnalyse.LuaAdjustClassFunc import LuaAdjustClassFunc
from Unity.app.services.UnityLuaAnalyse.LuaFuncStackLog import LuaFuncStackLog
from Unity.app.services.UnityLuaAnalyse.LuaRemoveComment import LuaRemoveComment
from Unity.app.services.UnityLuaAnalyse.LuaFormat import LuaFormat
import os
import shutil
from utils import sysUtils
from utils import pyServiceUtils
from utils import pyUtils
from utils import fileUtils


# 分析 lua 文件，修改其内容，为函数添加输出【最好配合Git，省得在单独备份文件】
class UnityLuaAnalyse(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        self.luaAdjustClassFunc: LuaAdjustClassFunc = None
        self.luaFuncStackLog: LuaFuncStackLog = None
        self.luaRemoveComment: LuaRemoveComment = None
        self.luaFormat: LuaFormat = None

    def create(self):
        super(UnityLuaAnalyse, self).create()
        self.luaAdjustClassFunc = self.getSubClassObject("LuaAdjustClassFunc")
        self.luaFuncStackLog = self.getSubClassObject("LuaFuncStackLog")
        self.luaRemoveComment = self.getSubClassObject("LuaRemoveComment")
        self.luaFormat = self.getSubClassObject("LuaFormat")
        # # 拷贝出来，展示结构
        # fileCopyUtils.copyFilesInFolderTo([".lua"], _baseFolderPath, "/disk/SY/farmNew/CodeAnalyse/Lua/Temp/Codes/", "include", True)
        #
        # # 移除掉所有的UTF-8前缀
        # for _filePath in folderUtils.getFileListInFolder("/disk/SY/farmNew/CodeAnalyse/Lua/Temp/Codes/"):
        #     fileUtils.removeBomInUTF8(_filePath)

    def addLuaRunningStackLogInFolder(self, luaFolderPath_: str):
        if not os.path.exists(luaFolderPath_):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), luaFolderPath_ + "不存在")
        print(f'{luaFolderPath_} 添加注释中')
        self.luaFormat.luaFormatInFolder(luaFolderPath_)  # 格式化
        print('    格式化结束')
        self.luaRemoveComment.luaRemoveCommentInFolder(luaFolderPath_, luaFolderPath_)
        print('    移除注释结束')
        self.luaAdjustClassFunc.checkLuaStyleInFolder(luaFolderPath_)
        print('    校验格式结束')
        self.luaFuncStackLog.addFuncStackLogInFolder(luaFolderPath_, luaFolderPath_)
        print('    添加日志结束')

    def addLuaRunningStackLogOnFile(self, luaFilePath_: str):
        if not os.path.exists(luaFilePath_):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), luaFilePath_ + "不存在")
        self.luaFormat.luaFormatOnFile(luaFilePath_)  # 格式化
        self.luaRemoveComment.luaRemoveCommentOnFile(luaFilePath_, luaFilePath_)
        self.luaAdjustClassFunc.checkLuaStyleOnFile(luaFilePath_)
        self.luaFuncStackLog.addFuncStackLogOnFile(luaFilePath_, luaFilePath_)

    # 把 LogUtils 同步到目标文件夹中
    def syncLogUtils(self, luaRootPath_: str):
        _logUtilsFilePath = sysUtils.folderPathFixEnd(self.resPath) + "LogUtils.lua"
        _targetLogUtilsFilePath = sysUtils.folderPathFixEnd(luaRootPath_) + "LogUtils.lua"
        # 没有日志文件就拷贝过去
        if not os.path.exists(_targetLogUtilsFilePath):
            shutil.copy(_logUtilsFilePath, _targetLogUtilsFilePath)

    # 将 生成的日志中，将当前方法和上一个方法的时间差 xx.xx MS 移动到上面一行，近似代表上一行的执行时间
    def fixLogTimeDiff(self, logPath_: str):
        if not os.path.exists(logPath_):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), f'{logPath_} 不存在')
        _lines = fileUtils.linesFromFile(logPath_)
        # 整理时间
        _codeLines = []
        _timeDict = {}
        _LineLength = len(_lines)
        for _i in range(_LineLength):
            _line = _lines[_i][:-1]  # 去掉回车
            if " - " in _line:
                _codeAndTime = _line.split(" - ")
                _codeLines.append(f'{_i + 1:>{10}} {_codeAndTime[0]}')
                # 第一行时间无用
                if _i != 0:
                    # 时间需要往前串一个序号
                    _timeDict[_i - 1] = _codeAndTime[1]
            else:
                _codeLines.append(f'{_i + 1:>{10}} {_line}')
        # 构建新行
        _lineNews = []
        # 筛选整理之后数据
        _lineHuges = []
        _lineBigs = []
        _lineSmalls = []
        for _idx in range(len(_codeLines)):
            _newLineStr = None
            if _idx in _timeDict:
                _timeStr = _timeDict[_idx]
                # 当前行有时间，就添加上
                _newLineStr = f'{_codeLines[_idx]} - {_timeStr}'
                _float = float(_timeStr.split(" MS")[0])
                # 判断时间长短，录入指定文件
                if _float > 10:
                    _lineHuges.append(_newLineStr)
                if _float > 1:
                    _lineBigs.append(_newLineStr)
                if _float > 0.1:
                    _lineSmalls.append(_newLineStr)
            else:
                _newLineStr = f'{_codeLines[_idx]}'
            _lineNews.append(_newLineStr)

        fileUtils.writeFileWithStr(logPath_ + "_TimeFix", "\n".join(_lineNews))
        fileUtils.writeFileWithStr(logPath_ + "_Time_Small", "\n".join(_lineSmalls))
        fileUtils.writeFileWithStr(logPath_ + "_Time_Big", "\n".join(_lineBigs))
        fileUtils.writeFileWithStr(logPath_ + "_Time_Huge", "\n".join(_lineHuges))

    def destroy(self):
        super(UnityLuaAnalyse, self).destroy()


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    _svr.fixLogTimeDiff("/disk/XS/C#Temp/Logs/LuaLog")
