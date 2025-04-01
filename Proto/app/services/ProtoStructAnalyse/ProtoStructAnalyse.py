#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import folderUtils
from utils import fileUtils
from utils import pyUtils
from utils import printUtils
from utils import pyServiceUtils
from Proto.app.services.ProtoStructAnalyse.ProtoStructInfo import ProtoStructInfo

import os


# proto 数据结构 解析生成 Hive 的 SQL 文件
# proto 解析，生成描述协议的文档。
class ProtoStructAnalyse(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

        self._tableRequireByOtherList = []  # 被引用的表
        self._enumTableList = []  # 枚举表
        self._tableFullNameDict = {}  # 全名表结构，所有表
        self._mainTableShortNameList = []  # 实际使用的主表，刨除了被引用表
        self._tableNameReqAndResList = []  # 一去一回表
        self._tableNameReqList = []  # 有去无回表
        self._tableNameResList = []  # 有回无去表
        self._tableNameOther = []  # 非请求访问表
        self.sep = "|      "
        self.protoStructInfo: ProtoStructInfo = None

    def create(self):
        super(ProtoStructAnalyse, self).create()
        self.protoStructInfo = self.getSubClassObject("ProtoStructInfo")

    def destroy(self):
        super(ProtoStructAnalyse, self).destroy()

    # 构建Proto结构，将结构内容返回成字符串列表
    # 这里的文件夹结构一定是
    # Folder
    # |____Type
    #      |____xxRes.proto
    #      |____xxReq.proto
    #      |____xxSync.proto
    # 这样的结构，嵌套的结构。
    # 将结构内容输出
    def analyseProtoStructureInFolder(self, protobufFolderPath_: str, filters_: list = None):
        if not filters_ is None:
            for _i in range(len(filters_)):
                _fileName = filters_[_i]
                if not _fileName.endswith(".proto"):
                    self.raiseError(pyUtils.getCurrentRunningFunctionName(), "过滤文件鄙视以 .proto 结尾")

        # 整个文件夹中的所有proto的结构
        self.buildProtoStructure(protobufFolderPath_, filters_)
        # 展开结构成结构列表，逐行保存成字符串数组
        _tableStructureStrList = self.expandTableStructureInFolderReqRes(protobufFolderPath_)
        return _tableStructureStrList

    # 将 proto 结构搞成 dict
    def printStructAsDict(self, prefix_: str, protoName_: str):
        _root = dict()
        self.getDictByTableInfo(_root, self._tableFullNameDict[protoName_])
        printUtils.printPyObjAsKV(prefix_ + protoName_, _root)

    def getDictByTableInfo(self, belongToDict_: dict, tableInfo_: dict):
        _propertyList = tableInfo_["propertyList"]
        for _i in range(len(_propertyList)):
            _property = _propertyList[_i]
            _dataType = _property["dataType"]
            _needType = _property["needType"]
            _propertyName = _property["propertyName"]
            # 普通
            if self.isNormalProperty(_dataType):
                belongToDict_[_propertyName] = _dataType
            else:
                # 字典 或 列表
                _newDict = dict()
                self.getDictByTableInfo(_newDict, self._tableFullNameDict[_dataType])
                if _needType == "repeated":
                    # 列表
                    _newList = list()
                    belongToDict_[_propertyName] = _newList
                    _newList.append(_newDict)
                else:
                    # 字典
                    belongToDict_[_propertyName] = _newDict

    # proto 的基本类型
    def isNormalProperty(self, dataType_):
        return (dataType_ == "int64") or \
            (dataType_ == "uint64") or \
            (dataType_ == "int32") or \
            (dataType_ == "uint32") or \
            (dataType_ == "string") or \
            (dataType_ == "bool") or \
            (dataType_ == "float") or \
            (dataType_ == "double") or \
            (dataType_ == "bytes")

    # # 结构转换成一个dict
    # def protoStructureToDict(self,tableInfo_:dict):

    # 文件夹内的所有文件中的protobuf定义的表，放到一个大字典中。
    def getTableInfoDictFormFolder(self, protoFolderPath_: str, filters_: list = None):
        _protoStructInfoDict = {}
        _filePathDict = folderUtils.getFilePathKeyValue(protoFolderPath_, [".proto"])
        for _protoFileName, _protoFilePath in _filePathDict.items():
            # 不在过滤内才分析
            if (filters_ is None) or (not (_protoFileName in filters_)):
                # 获取 文件 以及其内部的结构
                _keyName = fileUtils.justName(_protoFileName)
                _currentProtoInfo = self.protoStructInfo.getProtobufStructInfo(_protoFileName, _protoFilePath)
                _protoStructInfoDict[_keyName] = _currentProtoInfo

        # 表字典
        _tableDict = {}
        for _protoName, _protoSturct in _protoStructInfoDict.items():
            # 文件内的结构列表
            _tableList = _protoSturct["tableList"]
            for _table in _tableList:
                # 将当前文件内的结构，合并到全局表中
                _protoName = _table["protoName"]
                if _protoName in _tableDict:
                    _fileName1 = _tableDict[_protoName]["fileName"]
                    _fileName2 = _table["fileName"]
                    self.raiseError(pyUtils.getCurrentRunningFunctionName(),
                                    "已经存在proto定义 " + _protoName + " \n    " + _fileName1 + "\n    " + _fileName2
                                    )
                _tableDict[_protoName] = _table
        return _tableDict

    # 将结构展开打印
    def expandTableStructureInFolderReqRes(self, protobufFolder_: str):
        # 删
        return _structureStrList

    # 将结构展开打印
    def expandTableStructureInFolder(self, protobufFolder_: str):
        # 识别 文件夹 结构，按照文件夹的归属，输出proto分类和结构
        _folderList = folderUtils.getFolderNameListJustOneDepth(protobufFolder_)
        _folderList.sort()
        _structureStrList = []
        # 文件夹列表
        for _folder in _folderList:
            _structureStrList.append(str(_folder) + " --------------------------------------------------------")
            _fileList = folderUtils.getFileNameListJustOneDepth(os.path.join(protobufFolder_, _folder), [".proto"])
            _fileList.sort()
            _mainTableFullNameInFolderList = []
            # 文件列表
            for _file in _fileList:
                for _tableFullName, _tableInfo in self._tableFullNameDict.items():
                    # 作为主表的才需要输出结构
                    if _tableFullName in self._mainTableShortNameList:
                        # 主表文件名一致，标示查找到
                        if _tableInfo["fileName"] == _file:
                            _mainTableFullNameInFolderList.append(_tableFullName)
                            break
            _baseStr = " " * 4
            _findBoo = False
            _mainTableFullName = None
            for _tempFullName in self._tableNameReqAndResList:
                if _tempFullName in _mainTableFullNameInFolderList:
                    _mainTableFullName = _tempFullName
                    _findBoo = True
                    break
            if _findBoo:
                _structureStrList += self.expandTableStructure(_mainTableFullName, 0, _baseStr)
        return _structureStrList

    # 展开表
    def expandTableStructure(self, tableName_: str, depth_: int = 0, baseStr_: str = ""):
        # 删

    def buildProtoStructure(self, protoFolderPath_: str, filters_: list = None):
        _printInfo = False
        # 获取文件夹内所有proto文件定义的协议格式，做成键值对
        _tableDict = self.getTableInfoDictFormFolder(protoFolderPath_, filters_)
        # 表结构文件名 和 表结构内容 的循环
        for _shortTableName, _tableInfo in _tableDict.items():
            _protoName = _tableInfo["protoName"]
            # < 协议名 : 协议结构 > 缓存到当前运行时构成的键值表中
            self._tableFullNameDict[_protoName] = _tableInfo

        # 整理成全名字典
        for _tableFullName, _tableInfo in self._tableFullNameDict.items():
            _type = _tableInfo["type"]  # 获取 表的 类型
            if _type == "enum":
                if not (_tableFullName in self._enumTableList):
                    self._enumTableList.append(_tableFullName)  # 枚举类的记录到枚举列表中

            _common = ''
            if "common" in _tableInfo:
                _common = _tableInfo["common"]
            if _printInfo:
                print("{0} [{1}] - {2}".format(_tableFullName, _type, _common))

            if _type == "table" and 'propertyList' in _tableInfo:
                _propertyList = _tableInfo["propertyList"]
                for _property in _propertyList:
                    _propertyName = _property["propertyName"]
                    _needType = _property["needType"]
                    _dataType = _property["dataType"]
                    _index = _property["index"]
                    _common = _property["common"]
                    if not self.isNormalProperty(_dataType):
                        if not (_dataType in self._tableRequireByOtherList):
                            self._tableRequireByOtherList.append(_dataType)
                    if _printInfo:
                        print("    {0} : {1}[{2}/{3}] - {4}".format(_index, _propertyName, _dataType, _needType,
                                                                    _common))
            if _type == "enum" and 'propertyList' in _tableInfo:
                _propertyList = _tableInfo["propertyList"]
                for _property in _propertyList:
                    _propertyName = _property["propertyName"]
                    _index = _property["index"]
                    _common = _property["common"]
                    if _printInfo:
                        print("    {0} : {1} - {2}".format(_index, _propertyName, _common))

        if _printInfo:
            print("被引用的proto文件 ----------------------------------------")
            for _tableRequireByOther in self._tableRequireByOtherList:
                print(str(_tableRequireByOther))
            print("为枚举的文件 ---------------------------------------------")
            for _enumTable in self._enumTableList:
                print(str(_enumTable))

        for _tableName, _tableInfo in self._tableFullNameDict.items():
            if not (_tableName in self._tableRequireByOtherList):
                if not (_tableName in self._enumTableList):
                    self._mainTableShortNameList.append(_tableName)

        if _printInfo:
            print("为主文件 ---------------------------------------------")
        self._mainTableShortNameList.sort()

        _reqTableList = []
        _resTableList = []
        for _tableName in self._mainTableShortNameList:
            if _tableName.endswith("Req"):
                _reqTableList.append(_tableName)
            elif _tableName.endswith("Res"):
                _resTableList.append(_tableName)
            else:
                self._tableNameOther.append(_tableName)

        for _tableNameReq in _reqTableList:
            _tableNameRes = _tableNameReq.split("Req")[0] + "Res"
            if _tableNameRes in _resTableList:
                self._tableNameReqAndResList.append(_tableNameReq)
                self._tableNameReqAndResList.append(_tableNameRes)

        for _tableNameReq in _reqTableList:
            if not _tableNameReq in self._tableNameReqAndResList:
                self._tableNameReqList.append(_tableNameReq)

        for _tableNameRes in _resTableList:
            if not _tableNameRes in self._tableNameReqAndResList:
                self._tableNameResList.append(_tableNameRes)

        if _printInfo:
            print("    Req <-> Res ----------------------------------------")
            for _tableName in self._tableNameReqAndResList:
                print(_tableName)

            print("    Req -> ---------------------------------------------")
            for _tableName in self._tableNameReqList:
                print(_tableName)

            print("    Res <- ---------------------------------------------")
            for _tableName in self._tableNameResList:
                print(_tableName)

            print("    Others ---------------------------------------------")
            for _tableName in self._tableNameOther:
                print(_tableName)


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
