#!/usr/bin/env python3
# Created by BB at 2023/6/14
import json
import os

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils.puerTsDebugUtils import V8RuntimeExecutor
from utils import fileUtils
from utils import folderUtils
from utils import fileCopyUtils
from utils.CompanyUtil import Company_BB_Utils
from utils import cmdUtils

import sys

vmJsonFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/vmJson")
tsCodeFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/src")
unityFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_unity")
jsCodeFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/dist")
puerTsFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/dist/puerts/")
csCodeFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_unity/Assets/Scripts")
infosAndLogsPath = os.path.join(Company_BB_Utils.getSLGRoot(), "infosAndLogs/")

V8DebuggerPort = 8080


class BBTs_V8_Debugger(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(BBTs_V8_Debugger, self).create()

    def destroy(self):
        super(BBTs_V8_Debugger, self).destroy()

    def copyJSCode(self):
        _jsFromCodeFolder = os.path.join(jsCodeFolderPath, "Framework", "ABDebug")
        _jsToCodeFolder = os.path.join(self.subResPath, "ABDebug", "js")
        fileCopyUtils.copyFilesInDir(_jsFromCodeFolder, _jsToCodeFolder, False, [".js"])

        _jsToCodeFolder = os.path.join(self.subResPath, "ABDebug", "puerTs")
        fileCopyUtils.copyFilesInDir(puerTsFolderPath, _jsToCodeFolder, False, ["native.js", "modular.mjs"])

        _jsToCodeFolder = os.path.join(self.subResPath, "ABDebug", "TsDebug")
        fileCopyUtils.copyFilesInDir(os.path.join(tsCodeFolderPath, "Debug"), _jsToCodeFolder, False, ["Debug.ts"])

    def copyCSCode(self):
        _csFromCodeFolder = os.path.join(csCodeFolderPath, "ABDebug")
        _csToCodeFolder = os.path.join(self.subResPath, "ABDebug", "cs")
        fileCopyUtils.copyFilesInDir(_csFromCodeFolder, _csToCodeFolder, False, [".cs"])

    # 清理日志
    def clearLogs(self):
        folderUtils.deleteThenCreateFolder(os.path.join(unityFolderPath, "Logs"))
        _logPath = os.path.join(infosAndLogsPath, "Logs/PuertsLog")
        fileUtils.removeExistFile(_logPath)
        fileUtils.writeFileWithStr(_logPath, "")

    # 重置 TypeScript 环境
    def reset(self):
        self.exeCodeOnPort(V8DebuggerPort, '''
(() => {
    var __importDefault = (this && this.__importDefault) || function (mod) {
        return (mod && mod.__esModule) ? mod : { "default": mod };
    };
    let GameIns = __importDefault(require("./Game/Game")).default;
    GameIns.ResetToLaunch(); // 重开 js 环境
})();
        ''')

    # Tools 下的一些工具
    def debugTool(self, toolName_: str):
        _jsModuleCodeFolderPath = os.path.join(jsCodeFolderPath, "Framework", "ABDebug", "Tools")
        _debugJsPath = os.path.join(_jsModuleCodeFolderPath, f"{toolName_}.js")
        self.executeJsFile(V8DebuggerPort, _debugJsPath)

    # 打印当前的内存数据
    def dumpDataAndLayer(self):
        folderUtils.deleteThenCreateFolder(os.path.join(infosAndLogsPath, "DumpDataMock"))
        self.debugTool("DumpDataMock")
        folderUtils.deleteThenCreateFolder(os.path.join(infosAndLogsPath, "DumpLayer"))
        self.debugTool("DumpLayer")
        folderUtils.deleteThenCreateFolder(os.path.join(infosAndLogsPath, "DumpConfig"))
        self.debugTool("DumpConfig")

    # 执行 JS Debug
    def executeJsFile(self, port: int, jsCodePath_: str):
        self.exeCodeOnPortList(port, [fileUtils.readFromFile(jsCodePath_)])

    def exeCode(self, code: str):
        self.exeCodeOnPort(V8DebuggerPort, code)

    def exeCodeOnPort(self, port: int, code: str):
        self.exeCodeOnPortList(port, [f"(() => {{\n{code}\n}})();"])

    def exeCodeOnPortList(self, port: int, codeList: [str]):
        # 删

    def vmBtnEvtFile(self, moduleName_: str, vmJsonName_: str):
        jsonFilePath = os.path.join(vmJsonFolderPath, f"{vmJsonName_}.json")
        if not os.path.exists(jsonFilePath):
            return None, ""
        jsonContent = fileUtils.readFromFile(jsonFilePath)
        jsonDict = json.loads(jsonContent)
        vmPropertyDict = jsonDict["children"]
        codeStr = ""
        hasBtnEvt = False
        _ClassName = f'{vmJsonName_}Class'
        for _propName in vmPropertyDict:
            if "type" in vmPropertyDict[_propName] and vmPropertyDict[_propName]["type"] == "symbol":
                codeStr += f"    static {vmJsonName_}_{_propName} = {_ClassName}.{vmJsonName_}.{_propName}\n"
                hasBtnEvt = True
        if hasBtnEvt:
            return f'const {_ClassName} = require("../../../../Game/Module/{moduleName_}/VM/{vmJsonName_}")\n', codeStr
        else:
            return None, ""

    def vmBtnEvtFolder(self, moduleName_: str):
        _vmFilePathList = folderUtils.getFileNameListJustOneDepth(os.path.join(tsCodeFolderPath, "Game", "Module", moduleName_, "VM"))
        classAllStr = ""
        btnAllStr = ""
        for _i in range(len(_vmFilePathList)):
            _vmFilePath = _vmFilePathList[_i]
            _classStr, _btnStr = self.vmBtnEvtFile(moduleName_, fileUtils.justName(_vmFilePath))
            if _classStr is not None:
                classAllStr += _classStr
                btnAllStr += _btnStr

        codeStr = f'{classAllStr}class {moduleName_}VM {{\n{btnAllStr}}}\nexports.default = {moduleName_}VM;'
        jsModuleCodeFolderPath = os.path.join(jsCodeFolderPath, "Framework", "ABDebug", "Module", moduleName_)
        folderUtils.makeSureDirIsExists(jsModuleCodeFolderPath)
        fileUtils.writeFileWithStr(os.path.join(jsModuleCodeFolderPath, f'{moduleName_}VM.js'), codeStr)

    def debugModule(self, moduleName_):
        self.copyJSCode()  # 拷贝一下代码文件
        self.copyCSCode()
        self.vmBtnEvtFolder(moduleName_)
        _jsModuleCodeFolderPath = os.path.join(jsCodeFolderPath, "Framework", "ABDebug", "Module", moduleName_)
        _debugJsPath = os.path.join(_jsModuleCodeFolderPath, f"{moduleName_}Debug.js")
        self.executeJsFile(V8DebuggerPort, _debugJsPath)

    # 自动更换 Pid 登陆（新账户）
    def setOrAddPid(self, targetPid_=None):
        # 删

    # 重置新手引导
    def reGuide(self):
        self.clearLogs()  # 清理 MOCK
        self.setOrAddPid()  # 更换 pid
        self.debugTool("RelaunchWithNewPid")  # 执行重置pid并重启的工具

    def new_debugModule(self, moduleName_: str):
        self.exeCode(f'require("./Debug/{moduleName_}Debug", true)')
        # self.exeCode(f'require("./Framework/ABDebug/Module/{moduleName_}/{moduleName_}ReImport", true)')

    # 使用 beyondCompare 比较值变化
    def tryCompareVM(self, vmName_: str, verFrom_: int, verTo_: int):
        # 删


import asyncio
import nest_asyncio


async def waitForSecond(sec: int):
    await asyncio.sleep(sec)


if __name__ == '__main__':
    _subSvr: BBTs_V8_Debugger = pyServiceUtils.getSubSvr(__file__)
    pyServiceUtils.printSubSvrCode(__file__)

    sys.exit(1)

    # 拷贝一下代码文件
    _subSvr.copyJSCode()
    _subSvr.copyCSCode()
    # sys.exit(1)

    nest_asyncio.apply()

    # # 执行一下 模块的 Debug 文件
    # _subSvr.debugModule("HeroBag")
    # sys.exit(1)

    # 执行一下 Debug 文件
    # _subSvr.new_debugModule("HeroBag")
    # asyncio.run(waitForSecond(2))
    # _subSvr.tryCompareVM("MainGet", 1, 2)  # 比较可坑产生的 VM
    # sys.exit(1)

    # # 拷贝一下代码文件

    # sys.exit(1)

    # 修改一下pid
    _subSvr.reGuide()
