#!/usr/bin/env python3
# Created by BB at 2023/5/16
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import folderUtils
from utils import fileUtils
from utils import pyUtils
import re
import sys
import os
import shutil


class BBTs_AnalyseTs(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(BBTs_AnalyseTs, self).create()

    def destroy(self):
        super(BBTs_AnalyseTs, self).destroy()

    # 分析 csProject_ 中 ts 工程内 src 下的代码，使用 relativeFilterPartNameList_ 作为过滤项，isExclude_ = True 时排除、 = False 时囊括
    def analyseTS_addLog(self, csProject_: str, relativeFilterPartNameList_: list, isExclude_: bool = True):
        _tsProject = os.path.join(csProject_, "project_ts")
        _unityProject = os.path.join(csProject_, "project_unity")
        _tsPath = os.path.join(_tsProject, "src")

        # 判断是否已经分析过了
        if os.path.exists(os.path.join(_tsPath, "Framework", "LogUtils.ts")):  # 存在 日志 工具
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), "当前目录已经是分析后的目录")
            sys.exit(1)

        if not os.path.exists(os.path.join(_unityProject, "Assets", "Scripts", "LogUtils.cs")):  # CS 端的日志接口修改
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), "Unity 工程中没有 LogUtils.cs ，请 从 V8_Debugger 的 res 文件中拷贝")
            sys.exit(1)

        if not fileUtils.fileHasString(
                os.path.join(_unityProject, "Assets", "Scripts", "Framework", "Log", "Log.cs"),
                "LogUtils.HookLog(aLogStr,aLogLevel);"):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), "Unity 工程中没有 Log.cs ，并未修改")
            sys.exit(1)

        # # 确保 ts 监控开启，这样生成完毕，直接就拷贝到Unity中了
        # _watchCmd = "tsc --watch --project tsconfig.json"
        # if not cmdUtils.isCmdRunning(_watchCmd):
        #     cmdUtils.doStrAsCmd(_watchCmd, _tsProject)

        # 分析 ts 工程生成日志
        self.analyseTSFolder(_tsPath, relativeFilterPartNameList_, isExclude_)
        # 将生成日志后的内容直接刷给 Unity
        # [package.json].scripts.postinstall 指定了 npm install 后的脚本，可以将内容同步给Unity
        # cmdUtils.doStrAsCmd("npm install", _tsProject)

    def analyseTSFolder(self, tsProjectSrc: str, relativeFilterPartNameList_: list, isExclude_: bool):
        # 分析，并修改源码
        _filePathDict = folderUtils.getFilePathKeyValue(tsProjectSrc, [".ts"], True)
        for _, _filePath in _filePathDict.items():  # 相对路径
            _relativePath = _filePath.split("src" + os.sep)[1]
            _isPass = False
            for _i in range(len(relativeFilterPartNameList_)):
                # 排除 还是 囊括。
                # 排除就是列表中的不处理
                # 囊括就是只处理列表中的
                if (relativeFilterPartNameList_[_i] in _relativePath and isExclude_ is True) or (
                        not relativeFilterPartNameList_[_i] in _relativePath and isExclude_ is False
                ):
                    print(f"- pass - : {_relativePath}")
                    _isPass = True
            # 跳过
            if _isPass:
                continue
            else:
                print(f"analyse : {_relativePath}")
            _relativePathList = _relativePath.split(os.sep)
            _importStr = f'import LogUtils from "{(len(_relativePathList) - 1) * "../"}Framework/LogUtils";\n'
            self.analyseTSFile(_filePath, _relativePath, _importStr)

        shutil.copy(os.path.join(self.subResPath, "LogUtils.ts"), os.path.join(tsProjectSrc, "Framework", "LogUtils.ts"))  # 拷贝日志工具

    def analyseTSFile(self, tsFilePath_: str, relativePath_: str, importStr_: str):
        # 删


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils

    _csProject = Company_BB_Utils.getSLGProjectPath()
    # _relativeFilterPartNameList = [
    #     # "Framework/",
    #     # "Game/"
    # ]
    # # 分析并添加日志
    # _subSvr.analyseTS_addLog(_csProject, _relativeFilterPartNameList)

    _relativeFilterPartNameList = ["Game/Module/Science/"]
    # 剔除 指定名称文件 ，分析并添加日志
    _subSvr.analyseTS_addLog(_csProject, _relativeFilterPartNameList, False)
