#!/usr/bin/env python3
# Created by nobody at 2023/4/10
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import fileUtils
from utils import folderUtils
from utils import fileCopyUtils
import json
import os


class Assets_Export(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(Assets_Export, self).create()

    def destroy(self):
        super(Assets_Export, self).destroy()

    def exportFolderList(self, unityVersion_: int, projectPath_: str, relativePathList_: list, packagePath_: str):
        self.createJson(projectPath_, relativePathList_, packagePath_)
        self.copyCS(projectPath_)
        self.doCMD(unityVersion_, projectPath_)

    def createJson(self, projectPath_: str, relativePathList_: list, packagePath_: str):
        # 创建一个json文件，将参数写入，Unity 命令行执行时，解析这个 json。
        _configDict = dict()
        _configDict["relativePathList"] = relativePathList_
        _configDict["packagePath"] = packagePath_
        _jsonStr = str(json.dumps(_configDict, indent=4, sort_keys=False, ensure_ascii=False))
        # 配置文件，放置在 Unity 中的位置
        _tarJsonPath = os.path.join(projectPath_, "Assets", "PY_Service", "Assets_Export", "Assets_Export.json")
        fileUtils.writeFileWithStr(_tarJsonPath, _jsonStr)

    def copyCS(self, projectPath_: str):
        # 拷贝要执行的 CS 脚本
        _csSrcFilePath = os.path.join(self.subResPath, "Assets_Export.cs")  # 可执行文件路径
        _csTarFolderPath = os.path.join(projectPath_, "Assets", "PY_Service", "Assets_Export")
        folderUtils.makeSureDirIsExists(_csTarFolderPath)  # 确保文件目录存在s
        _csTarFilePath = os.path.join(_csTarFolderPath, "Assets_Export.cs")  # 目标路径
        fileCopyUtils.copyFile(_csSrcFilePath, _csTarFilePath)  # 拷贝文件到指定目录

    def doCMD(self, unityVersion_: int, projectPath_: str):
        # 实际执行 当前服务命令
        _unityPath = self.belongToService.getUnityAppPath(unityVersion_)
        # 命令行
        _cmdList = [
            _unityPath,
            "-projectPath",
            projectPath_,
            '-quit',  # 其他命令执行完毕后将退出Unity编辑器。
            '-batchmode',  # 批处理模式下运行Unity
            '-executeMethod',  # 执行方法
            'Assets_Export.doCMD'  # 导出方法
        ]
        _cmdStr = " ".join(_cmdList)
        print('执行命令 : ' + str(_cmdStr))


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
