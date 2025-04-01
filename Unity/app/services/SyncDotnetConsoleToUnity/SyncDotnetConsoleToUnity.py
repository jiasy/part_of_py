#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import fileUtils
from utils import folderUtils
from utils import printUtils
from utils import fileCopyUtils
import os
import sys
from utils.infoUtils.InfoColor import InfoColor


class SyncDotnetConsoleToUnity(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(SyncDotnetConsoleToUnity, self).create()

    def destroy(self):
        super(SyncDotnetConsoleToUnity, self).destroy()

    # 将 dotnet console 的 cs 脚本，同步代码到 Unity 中
    def syncConsoleToUnity(self, dotnetConsoleFolder_: str, unityProjectFolder_: str):
        if not os.path.exists(dotnetConsoleFolder_):
            print(f"ERROR : {dotnetConsoleFolder_} not exists.")
            sys.exit(1)
        if not os.path.exists(unityProjectFolder_):
            print(f"ERROR : {unityProjectFolder_} not exists.")
            sys.exit(1)

        # 获取 命名空间 csproj 的名称是命名空间名，也就是拷贝到Unity时的文件夹名称
        _csprojName = folderUtils.getFileNameListJustOneDepth(dotnetConsoleFolder_, [".csproj"])[0]
        _nameSpace = fileUtils.justName(_csprojName)
        printUtils.pTitleLog("nameSpace : ", _nameSpace)

        # 获取 Unity 的 代码放置路径，并同步代码
        _unityScriptFolder = os.path.join(unityProjectFolder_, "Assets", "Scripts")
        if not os.path.exists(_unityScriptFolder):
            print(f"ERROR : {_unityScriptFolder} not exists.")
            sys.exit(1)

        printUtils.pTitleError(" 同步代码 ", ' ------------------------ ', [InfoColor.Blue])
        printUtils.pWarn(f" 同步 Assets/Scripts/{_nameSpace}", [InfoColor.Blue, InfoColor.Red])
        _unityNameSpaceFolder = os.path.join(_unityScriptFolder, _nameSpace)  # 代码持有的命名空间
        folderUtils.deleteThenCreateFolder(_unityNameSpaceFolder)  # 确保所有内容都是同步的
        fileCopyUtils.copyFilesInFolderTo([".cs"], dotnetConsoleFolder_, _unityNameSpaceFolder)  # 保持当前的文件夹结构将文本同步过去

        printUtils.pWarn(" 删除 fake UnityEngine", [InfoColor.Blue, InfoColor.Red])
        _fackUnityEngineFolder = os.path.join(_unityNameSpaceFolder, "UnityEngine")  # console 中模拟 Unity 环境的代码
        folderUtils.removeTree(_fackUnityEngineFolder)  # 删除掉模拟代码

        printUtils.pWarn(" 删除 obj", [InfoColor.Blue, InfoColor.Red])
        _objFolder = os.path.join(_unityNameSpaceFolder, "obj")  # console 中 CSharp 的环境依赖
        folderUtils.removeTree(_objFolder)  # 删除掉模拟代码

        printUtils.pWarn(" 删除 Program.cs", [InfoColor.Blue, InfoColor.Red])
        _programFile = os.path.join(_unityNameSpaceFolder, "Program.cs")
        fileUtils.removeExistFile(_programFile)

        printUtils.pWarn(" 添加 System 引用，并设置成只读", [InfoColor.Blue, InfoColor.Red])
        _csFilePathList = folderUtils.getFileListInFolder(_unityNameSpaceFolder, [".cs"])
        _importPathStr = 'using System;\nusing System.Collections.Generic;\nusing System.IO;\nusing System.Linq;\nusing System.Threading;\n'
        for _i in range(len(_csFilePathList)):
            _csFilePath = _csFilePathList[_i]  # 添加 两行引用
            fileUtils.writeFileWithStr(_csFilePath, _importPathStr + fileUtils.readFromFile(_csFilePath))
            # fileUtils.setFileToReadOnly(_csFilePathList[_i])

        printUtils.pTitleError(" 拷贝资源 ", ' ------------------------ ', [InfoColor.Blue])
        _unityResFolder = os.path.join(unityProjectFolder_, "Assets", "Resources")
        if not os.path.exists(_unityResFolder):
            print(f"ERROR : {_unityResFolder} not exists.")
            sys.exit(1)

        printUtils.pWarn(" 同步 json、bytes", [InfoColor.Blue, InfoColor.Red])
        _consoleResFolder = os.path.join(dotnetConsoleFolder_, "Resources")
        if not os.path.exists(_consoleResFolder):
            print(f"ERROR : {_consoleResFolder} not exists.")
            sys.exit(1)
        fileCopyUtils.copyFilesInFolderTo([".json", ".bytes"], _consoleResFolder, _unityResFolder)


if __name__ == '__main__':
    _svr_SyncDotnetConsoleToUnity: SyncDotnetConsoleToUnity = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_SyncDotnetConsoleToUnity.resPath))
    pyServiceUtils.printSvrCode(__file__)

    _svr_SyncDotnetConsoleToUnity.syncConsoleToUnity(
        "/Users/nobody/Documents/develop/GitHub/Services/CS_Service/",
        "/Users/nobody/Documents/develop/GitRepository/Unity_2023_2D_UPR/"
    )
