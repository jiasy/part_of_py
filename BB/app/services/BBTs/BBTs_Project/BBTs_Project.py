#!/usr/bin/env python3
# Created by BB at 2023/5/19
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
import os
from utils.CompanyUtil import Company_BB_Utils
from Excel.app.services.Svn import Svn
from enum import Enum
from utils import cmdUtils
from utils import fileUtils
from utils import printUtils
from collections import OrderedDict
import subprocess
from BB.app.services.BBTs.BBProtoStructTS import defaultLogicVmLayer, BBProtoStructTS


# 库类型
class PathType(Enum):
    NONE = 0
    DEV = 1  # 开发
    REL = 2  # 发布


class ModuleType(Enum):
    NONE = 0
    COMMON = 1  # 公用
    NORMAL = 2  # 常规
    ACT_INTER = 3  # 内置活动
    ACT_WEB = 4  # WEB 活动


'''
'''

_devProjectPath = Company_BB_Utils.getSLGProjectPath()


class BBTs_Project(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.sourceCompareAppPath = "/Applications/Beyond\ Compare.app/Contents/MacOS/bcomp"  # 比较工具位置
        self.recoverProtoFolderPath = "/Users/XS/Downloads/proto/"  # proto 3 还原成 2 放置的位置
        self.targetProtoFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "proto/protofile/net/")  # proto 文件放置位置
        self.projectTSFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/")  # TS 工程路径
        self.relativeModuleFolderPath = "src/Game/Module/"  # 所有模块的文件夹相对 TS 的路径
        self.infosAndLogFolderPath = os.path.join(Company_BB_Utils.getSLGRoot(), "infosAndLogs/Infos/")  # 生成代码放置路径
        self.moduleFolderPath = os.path.join(self.projectTSFolderPath, self.relativeModuleFolderPath)  # 所有模块的文件夹
        self.protobufDescribeFolder = os.path.join(Company_BB_Utils.getSLGRoot(), "infosAndLogs/ProtobufInfo/")

        self.project_ts_path = os.path.join(_devProjectPath, "project_ts")  # ts 脚本工程
        self.project_proto_path = os.path.join(_devProjectPath, "proto", "protofile", "net")  # protobuf 工程
        self.svnTool: Svn = pyServiceUtils.getSvrByName("Excel", "Svn")

        # 创建 代码生成器
        self.bbProtoStructTS: BBProtoStructTS = pyServiceUtils.getSubSvrByName("BB", "BBTs", "BBProtoStructTS")
        self.bbProtoStructTS.recoverProtoFolderPath = self.recoverProtoFolderPath
        self.bbProtoStructTS.targetProtoFolderPath = self.targetProtoFolderPath
        self.bbProtoStructTS.projectTSFolderPath = self.projectTSFolderPath
        self.bbProtoStructTS.relativeModuleFolderPath = self.relativeModuleFolderPath
        self.bbProtoStructTS.infosAndLogFolderPath = self.infosAndLogFolderPath
        self.bbProtoStructTS.moduleFolderPath = self.moduleFolderPath
        self.bbProtoStructTS.protobufDescribeFolder = self.protobufDescribeFolder

    def create(self):
        super(BBTs_Project, self).create()

    def destroy(self):
        super(BBTs_Project, self).destroy()

    # 获取 模块 路径
    def ts_path_module(self, moduleName_: str):
        return os.path.join(self.project_ts_path, "src/Game/Module/", moduleName_)

    # 获取 Layer 路径
    def ts_path_module_layer(self, moduleName_: str):
        return os.path.join(self.project_ts_path, "src/Game/Module/", moduleName_, "Layer")

    # 创建名为 layerName_ 的 Layer
    def ts_try_create_module_layer(self, moduleName_: str, layerName_: str):
        _targetLayerTSPath = os.path.join(self.ts_path_module_layer(moduleName_), f"{layerName_}.ts")
        if not os.path.exists(_targetLayerTSPath):  # 不存在才创建，以免覆盖
            print('页面 创建 : ' + str(layerName_))
            _cmdStr = f"node scripts/newLayerScript.js {moduleName_} {layerName_}"  # 创建 Layer 的工具命令
            cmdUtils.doStrAsCmd(_cmdStr, self.project_ts_path)  # 工具只能在 project_ts 目录下运行
        else:
            print('页面 已 存在 : ' + str(layerName_))

    def ts_create_layer(self, moduleName_: str, uiLayerNameList_: list[str]):
        for _i in range(len(uiLayerNameList_)):
            defaultLogicVmLayer.createLayerVMCode(os.path.join(self.subResPath, "CodeTemplate"), self.moduleFolderPath, moduleName_, uiLayerNameList_[_i])

    # 创建名为 moduleName_ 的模块
    def ts_create_module(self, moduleName_: str, _comment: str, _moduleID: int, _pageList: list, protoName_: str):
        # 删

    # 创建指定名称的 proto
    def ts_try_create_proto(self, moduleName_: str):
        _targetProtoPath = os.path.join(self.project_proto_path, f"{moduleName_}.proto")
        if not os.path.exists(_targetProtoPath):
            print(f'空 proto 创建 : {moduleName_}，移步 jsonUtils.ipynb 中进行结构初创')
            fileUtils.writeFileWithStr(_targetProtoPath, "")
        else:
            print(f'proto 已 存在 : {moduleName_} - {_targetProtoPath}')
            if fileUtils.readFromFile(_targetProtoPath) == "":
                print(f'空 proto 创建 : {moduleName_}，移步 jsonUtils.ipynb 中进行结构初创')

    def getCompareCmd(self, moduleFolder_: str, moduleName_: str, type_: str):
        # 删

    # 打印 模块 所需比较的生成代码。因为这些代码没直接覆盖
    def doCompareCmd(self, moduleNameList_: str):
        # 先启动 app，免得后续命令行每执行一次，启动关闭一次
        subprocess.call(self.sourceCompareAppPath.replace("\ ", " "))
        _cmdStr = ""
        for _i in range(len(moduleNameList_)):
            _moduleName = moduleNameList_[_i]
            _currentModuleFolderPath = os.path.join(self.moduleFolderPath, _moduleName)
            _cmdStr += self.getCompareCmd(_currentModuleFolderPath, _moduleName, "Module")
            _cmdStr += self.getCompareCmd(_currentModuleFolderPath, _moduleName, "Data")
            _cmdStr += self.getCompareCmd(_currentModuleFolderPath, _moduleName, "Service")
            _cmdStr += self.getCompareCmd(_currentModuleFolderPath, _moduleName, "Mock")
        cmdUtils.doStrAsCmd(_cmdStr, self.projectTSFolderPath)


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _bbProject: BBTs_Project = pyServiceUtils.getSubSvr(__file__)
    print('_bbProject.subResPath = ' + str(_bbProject.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    # _moduleName = "QuickQueue"
    # _comment = "快捷队列"
    # _moduleID = None  #
    # _pageList = [
    #     f"{_moduleName}Layer",  # 工具一定会创建一个同名的
    # ]
    # _protoList = [
    #     _moduleName  # 有proto的话，按照规范，会有一个同名的
    # ]
    # _bbProject.ts_create_module(_moduleName, _comment, _moduleID, _pageList, _protoList)

    # _moduleName = "Rank"
    # _comment = "排行榜"
    # _moduleID = None  #
    # _pageList = [
    #     "RankNormalLayer",
    #     "RankAlliancePowerLayer",
    #     "RankPersonalPowerLayer",
    #     "RankAlliancePersonalPowerLayer",
    #     "RankAlliancePersonalDonateLayer",
    # ]
    # _protoList = [
    #     "RankList"
    # ]
    # _bbProject.ts_create_module(_moduleName, _comment, _moduleID, _pageList, _protoList)

    _moduleName = "LordInfo"
    _comment = "领主信息"
    _moduleID = None  #
    _pageList = [
        "LordInfoLayer",  # 领主信息
        "LordInfoMainLayer",  # 领主信息主页
        "LordActivityLayer",  # 领主信息主页 - 行动力提示
        "LordChangeNameLayer",  # 领主信息主页 - 领主更名
        "LordInfoOperateLayer",  # 领主信息主页 - 其他领主操作
        "LordHeadLayer",  # 领主头像 -
        "LordTroopsTipsLayer",  # 领主 - tip
        "LordTroopsLayer",  # 领主部队
        "LordTroopsDissolveLayer",  # 领主部队 - 遣散
    ]
    # _bbProject.ts_create_module(_moduleName, _comment, _moduleID, _pageList, "User")
    # _bbProject.ts_create_module(_moduleName, _comment, _moduleID, _pageList, "MarchFormation")
    _bbProject.ts_create_module(_moduleName, _comment, _moduleID, _pageList, "Barracks")
    # _bbProject.ts_create_module(_moduleName, _comment, _moduleID, _pageList, "Slg")
