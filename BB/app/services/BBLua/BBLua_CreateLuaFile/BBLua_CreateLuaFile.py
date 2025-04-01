#!/usr/bin/env python3
# Created by BB at 2023/2/15
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils.CompanyUtil import Company_BB_Utils
import os
from utils import folderUtils
from utils import strUtils
from utils import fileUtils
from utils import fileContentOperateUtils
from utils import pyUtils
from utils import printUtils
from utils import fileCopyUtils
from utils import listUtils
import sys
from enum import IntEnum
from Proto.app.services.ProtoStructAnalyse import ProtoStructAnalyse
from BB.app.services.BBLua.BBProtoStructLua import BBProtoStructLua
from Proto.app.services.ProtoStructAnalyse.ProtoStructInfo import ProtoStructInfo
from utils import dictUtils

from BB.app.services.BBLua.BBLua_CreateLuaFile import BBLua_ModuleConfig


class LogicType(IntEnum):
    NORMAL = 1  # 功能
    WEB = 2  # web 活动
    INTRNAL = 3  # 内置活动


_projectPath = Company_BB_Utils.getDebugProjectFolderPath()
_lua_rootPath = os.path.join(_projectPath, "Assets", "Dev", "Lua")
_logic_rootPath = os.path.join(_lua_rootPath, "Game", "Module", "logic")
_data_rootPath = os.path.join(_lua_rootPath, "Game", "Module", "data")
_service_rootPath = os.path.join(_lua_rootPath, "Game", "Module", "service")
_page_rootPath = os.path.join(_lua_rootPath, "ui", "page")
_protobuf_rootPath = Company_BB_Utils.getPJProtobufFolderPath()


class BBLua_CreateLuaFile(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(BBLua_CreateLuaFile, self).create()

    def destroy(self):
        super(BBLua_CreateLuaFile, self).destroy()

    def addItemToDict(self, item_, key_, dict_):
        if not key_ in dict_:
            dict_[key_] = list()
        dict_[key_].append(item_)

    # 生成 模块 的 lua 文件
    def createLuaForUI(self, pageName_, moduleName_, isForceCreate_):
        _page_folderPath = os.path.join(
            _page_rootPath, moduleName_)  # ui 所在文件夹
        _luaFilePath = os.path.join(_page_folderPath, pageName_ + ".lua")
        _typeStr = "page"  # 默认是 page
        if pageName_.endswith("Section"):
            _typeStr = "section"
        elif pageName_.endswith("Panel"):
            _typeStr = "panel"
        elif pageName_.endswith("Page"):
            _typeStr = "page"
        elif pageName_.endswith("Item"):
            _typeStr = "item"

        if not os.path.exists(_luaFilePath) or isForceCreate_:
            print("        " + _typeStr + " create")
            _templeteFilePath = os.path.join(
                self.subResPath, "ui_" + _typeStr + "_templete")  # 获取相应的模板
            _content = fileUtils.readFromFile(_templeteFilePath)
            _content = _content.format(moduleName=moduleName_)
            fileUtils.writeFileWithStr(_luaFilePath, _content)
        else:
            print("        " + _typeStr + " pass")

    # 根据信息创建类
    def createLuaForModule(self,
                           moduleName_: str,
                           metaNameList_: list,
                           pageList_: list,
                           logicType_: str,
                           common_: str,
                           isForceCreate_: bool = False
                           ):
        # 删

    def addCode(self, type_, filePath_, content_, replaceMark_, search_: str = None):
        # 确定用来判断是否已经写入的搜索文本
        _searchStr = search_
        if _searchStr == None:
            _searchStr = content_
        # 没有创建过
        if not fileUtils.fileHasString(filePath_, _searchStr):
            print(("        " + type_ + " create  - ").ljust(40) +
                  filePath_.split("Assets")[1])
            print("            " + filePath_)
            print("                " + content_)
            # 创建一次
            if not fileContentOperateUtils.replaceContent(
                    filePath_,
                    replaceMark_,
                    content_ + "\n" + replaceMark_
            ):
                printUtils.pError("ERROR : " + type_ + " 中未查找到锚点位置")
                sys.exit(1)
        else:
            print(("        " + type_ + " pass - ").ljust(40) +
                  filePath_.split("Assets")[1])

    # 修改 Logic、service、data 的初始化
    def addInitCode(self, moduleName_: str, logicType_: str, funcID_: int, actID_: int, common_: str):
        # 删

    # 根据 proto 生成 service 代码
    def addServiceCode(self, moduleName_, protoNameList_):
        _service_folderPath = os.path.join(_service_rootPath, moduleName_)
        _service_filePath = os.path.join(_service_folderPath, moduleName_ + "Service.lua")
        _service_content = fileUtils.readFromFile(_service_filePath)
        # SAMPLE - 用数组中的内容去切分字符串
        _service_split = strUtils.splitByList(_service_content,
                                              [
                                                  "-- map start --\n",
                                                  "-- map end --\n",
                                                  "-- func start --\n",
                                                  "-- func end --\n"
                                              ]
                                              )
        # 代码拆分成以下构成，修改后在合并回来
        _service_content_map = _service_split[0]
        _struct_all_content = ""
        _service_content_map_func = _service_split[2]
        _func_all_content = ""
        _service_content_func = _service_split[4]

        # 创建 其他 app 下的子服务
        _bbProtoStruct: BBProtoStructLua = pyServiceUtils.getSubSvrByName("BB", "BBLua", "BBProtoStruct")

        # proto 的列表
        _protoName = protoNameList_[0]
        # 添加 proto 初始化
        _proto_init_filePath = os.path.join(_lua_rootPath, "net", "ProtobufTypeManager.lua")
        _proto_init_initContent = "{protoName}_pb = require \"net.protobuflua.{protoName}_pb\"".format(protoName=_protoName)
        _proto_init_replaceMarkContent = "sevendaysin_pb = require \"net.protobuflua.sevendaysin_pb\""
        self.addCode("proto_init", _proto_init_filePath, _proto_init_initContent, _proto_init_replaceMarkContent)

        print("        add " + _protoName + "'s code.")
        _protofilePath = os.path.join(_protobuf_rootPath, "net", _protoName + ".proto")
        _struct_content, _func_content, _rspOrSyncStructNameList = _bbProtoStruct.createStructAndFuncCode(moduleName_, _protofilePath)
        _struct_all_content = _struct_all_content + _struct_content
        _func_all_content = _func_all_content + _func_content
        # 生成结构对应的lua代码（为这个结构构建一个lua数据）
        _luaServerSimulationList = []  # 模拟服务器的代码
        _luaCodeList = []  # 使用服务器数据的代码
        _serverPath = "_dataServer."
        for _idxLoop in range(len(_rspOrSyncStructNameList)):
            # 只在 接受 和 同步 消息处整理结构，主要用于前端的 测试 和 复制粘贴。
            _structName = _rspOrSyncStructNameList[_idxLoop]
            _root = dict()
            _bbProtoStruct.belongToService.getDictByTableInfo(_root, _bbProtoStruct.belongToService._tableFullNameDict[_structName])
            # 将 _root 解析成键值对模式，然后将键值对变换成创建此数据结构的 lua 代码
            _tempLuaCodeList = []
            dictUtils.createDictAsLua(
                _root, (_serverPath + _structName).format(moduleName=moduleName_),
                True,
                _tempLuaCodeList
            )
            # 模拟消息协议结构
            for _luaIdx in range(len(_tempLuaCodeList)):
                _findIdx = _tempLuaCodeList[_luaIdx].find("\{\}")
                _findIdx = _tempLuaCodeList[_luaIdx].find("{}")
                # 不记录声明结构的代码行
                if _findIdx < 0:
                    _luaCodeList.append(_tempLuaCodeList[_luaIdx])
            _luaCodeList.append("")
            # 协议结构
            _luaServerSimulationList.append("local {structName} = {{}}".format(structName=_structName))
            for _luaIdx in range(len(_tempLuaCodeList)):
                _luaServerSimulationList.append(_tempLuaCodeList[_luaIdx])
            _luaServerSimulationList.append("Data.{moduleName}Data:onServer(\"{structName}\", {structName})".format(moduleName=moduleName_, structName=_structName))
            _luaServerSimulationList.append("")

        for _idxLoop in range(len(_luaServerSimulationList)):
            _luaServerSimulationList[_idxLoop] = _luaServerSimulationList[_idxLoop].replace(_serverPath, "")
        _final_content = _service_content_map + "-- map start --\n" + _struct_all_content + "-- map end --\n" + \
                         _service_content_map_func + "-- func start --\n" + \
                         _func_all_content + "-- func end --\n" + _service_content_func
        fileUtils.writeFileWithStr(_service_filePath, _final_content)
        return listUtils.joinToStr(_luaCodeList, "\n"), listUtils.joinToStr(_luaServerSimulationList, "\n")

    # 显示 proto 的结构
    def showProtoStruct(self, moduleName_: str, protoNameList_: list):
        # 删

    # 打印一个 proto 文件的结构
    def showSingleProtoInfo(self, protoPath_: str, ):
        # 创建 其他 app 下的子服务
        _protoStructInfo: ProtoStructInfo = pyServiceUtils.getSubSvrByName(
            "ExcelWorkFlow",
            "ProtoStructAnalyse",
            "ProtoStructInfo"
        )
        _protoInfo = _protoStructInfo.getProtobufStructInfo(
            os.path.basename(protoPath_), protoPath_)
        printUtils.printPyObjAsKV(fileUtils.justName(protoPath_), _protoInfo)

    def createCode(self, moduleName_: str):
        _logicType, _pageList, _protoList, _protoStructList, _funcID, _activityID, _common = BBLua_ModuleConfig.getConfigByName(moduleName_)
        self.createCodeDetail(moduleName_, _logicType, _pageList, _protoList, _protoStructList, _funcID, _activityID, _common)

    def createCodeDetail(self, moduleName_, logicType_, pageList_, protoList_, protoStructList_, funcID_, activityID_, common_):
        # 删


# 获取自己对应的资源RichManInfo
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)

    # _moduleName = "CrossBoss"  # 跨服Boss战设置
    # _moduleName = "MonthCardTW"  # 台湾月卡
    # _moduleName = "LoginReward"  # 台湾登陆奖励
    # _moduleName = "DailyRecharge"  # 每日首充
    _moduleName = "TreatyGift"  # 缔约之礼

    _subSvr.createCode(_moduleName)
