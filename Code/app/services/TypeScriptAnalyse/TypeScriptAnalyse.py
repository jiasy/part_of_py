#!/usr/bin/env python3
import sys

from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import folderUtils
from utils import printUtils
from utils import fileUtils
from utils import fileContentOperateUtils
from utils import cmdUtils
import os
import time


# TypeScript 的解析，使用 typescript 自身的工具链
class TypeScriptAnalyse(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(TypeScriptAnalyse, self).create()

    def destroy(self):
        super(TypeScriptAnalyse, self).destroy()

    # 初始化一个 TS 工程
    def initTypeScriptProject(self, nameSpace_: str):
        if nameSpace_ == "support":
            print(f"ERROR : {nameSpace_} 关键字")
            sys.exit(1)
        _tsProjectRoot = os.path.join(self.resPath, nameSpace_)
        folderUtils.makeSureDirIsExists(_tsProjectRoot)

        # 没有 package.json ，执行 js 相关初始化
        _packageJsonFile = os.path.join(_tsProjectRoot, "package.json")
        if not os.path.exists(_packageJsonFile):
            print(f"{_tsProjectRoot} 中 变向 执行 npm init")  # 拷贝 package.json 相当于 npm init，省去命令行问答环节
            _supportPackageJson = os.path.join(self.resPath, "support", "package.json")  # 模板
            _nsPackageJson = os.path.join(_tsProjectRoot, "package.json")  # 目标位置
            fileUtils.copyTo(_supportPackageJson, _nsPackageJson)  # 模板拷贝到目标位置
            fileContentOperateUtils.replaceContent(_nsPackageJson, "nameSpace", nameSpace_)  # 替换掉内容
            cmdUtils.doStrAsCmd("npm install typescript ts-node --save-dev", _tsProjectRoot)  # 安装 typescript 支持
            cmdUtils.doStrAsCmd("npm install -g tsc-watch", _tsProjectRoot)  # 安装 tsc-watch 代替 tsc watch 命令，提升速度

        # 没有 tsconfig.json ，执行 ts 相关初始化
        _nsTsConfigJson = os.path.join(_tsProjectRoot, "tsconfig.json")
        if not os.path.exists(_nsTsConfigJson):
            cmdUtils.doStrAsCmd("npx tsc --init", _tsProjectRoot)  # typeScript 工程初始化
            _supportTsConfigJson = os.path.join(self.resPath, "support", "tsconfig.json")  # 模板
            fileUtils.copyTo(_supportTsConfigJson, _nsTsConfigJson)  # 模板拷贝到目标位置
            _indexTs = os.path.join(_tsProjectRoot, "index.ts")  # 入口文件，有它才能进行 node 命令行
            fileUtils.writeFileWithStr(_indexTs, "")

    # 添加 TS 分析工具
    def addToolTo(self, nameSpace_: str, toolName_: str):
        _tsAnalyseToolSrc = os.path.join(self.resPath, "support", "Tools", f"{toolName_}.ts")
        if not os.path.exists(_tsAnalyseToolSrc):
            print(f"ERROR : {toolName_} 不存在。")
            sys.exit(1)
        _tsAnalyseToolTarFolder = os.path.join(self.resPath, nameSpace_, "src", "Tools")
        folderUtils.makeSureDirIsExists(_tsAnalyseToolTarFolder)
        _tsAnalyseToolTar = os.path.join(_tsAnalyseToolTarFolder, f"{toolName_}.ts")
        if os.path.exists(_tsAnalyseToolTar):
            print(f"ERROR : {toolName_} 工程内已存在。")
            sys.exit(1)
        fileUtils.copyTo(_tsAnalyseToolSrc, _tsAnalyseToolTar)

    # 在哪个 nameSpace_ 下解析 projectFolder_ 中的 relativeTsPath_ 文件
    def doToolIn(self, nameSpace_: str, toolName_: str, paramList_: list[str] = None):
        _tsAnalyseToolRelativePath = os.path.join("Tools", f"{toolName_}.ts")  # 相对路径
        _tsProjectFolder = os.path.join(self.resPath, nameSpace_)  # 工程路径
        _tsAnalyseToolTar = os.path.join(_tsProjectFolder, "src", _tsAnalyseToolRelativePath)
        if not os.path.exists(_tsAnalyseToolTar):  # 没有
            self.addToolTo(nameSpace_, toolName_)  # 添加工具
        self.getTsResult(nameSpace_, _tsAnalyseToolRelativePath, paramList_)

    # 得到相对路径文件的执行结果
    def getTsResult(self, nameSpace_: str, tsRelativePath_: str, paramList_: list[str] = None):
        _tsProjectPath = os.path.join(self.resPath, nameSpace_)
        _tsPath = os.path.join(_tsProjectPath, "src", tsRelativePath_)
        if not os.path.exists(_tsPath):
            print(f"ERROR : {tsRelativePath_} not exist.")
            sys.exit(1)

        # ts 转换成 js 文件的路径
        _relativeRealJsPath = os.path.join("dist", tsRelativePath_).replace('.ts', '.js')

        # 10 秒内等执行命令的结果
        _watchCmd = 'tsc-watch'  # 当命令行出现了指定文本或结束
        _result = cmdUtils.run_command_threading(_watchCmd, _tsProjectPath, 10, "Found 0 errors. Watching for file changes.")

        if cmdUtils.isCmdRunning(_watchCmd):
            cmdUtils.killCmd(_watchCmd)  # 终结命令

        if _result is False:
            printUtils.pError("ERROR : 超时")
            sys.exit(1)

        # 拼接参数
        _paramStr = ""
        if paramList_ is not None:
            for _i in range(len(paramList_)):
                _paramStr = f"{_paramStr} '{paramList_[_i]}'"

        # 去工程所在的路径
        os.chdir(_tsProjectPath)
        _cmd = f'node {_relativeRealJsPath}{_paramStr}'  # 这时一定是最新的js
        _pipeLines = cmdUtils.doStrAsCmdAndGetPipeline(_cmd, _tsProjectPath)  # 在这里工程文件夹内执行js代码
        for _i in range(len(_pipeLines)):
            print(_pipeLines[_i])


if __name__ == '__main__':
    _svr: TypeScriptAnalyse = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
    # 创建工程
    _svr.initTypeScriptProject("AnalyseTS")
    # 在工程内添加工具并执行
    _svr.doToolIn(
        "AnalyseTS",
        "TsAnalyse",
        [
            "/disk/XS/SLG/DEV/projects/cs/project_ts/src/",
            "Game/Module/Science/VM/VMResearchConfirm.ts"
        ]
    )
