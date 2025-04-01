import utils.printUtils
from Proto.app.services.ProtoStructAnalyse import ProtoStructAnalyse
import logging
import sys
from utils import pyServiceUtils

protobuf_to_typescript_type_map = {
    "double": "number",
    "float": "number",
    "int32": "number",
    "int64": "number",
    "uint32": "number",
    "uint64": "number",
    "sint32": "number",
    "sint64": "number",
    "fixed32": "number",
    "fixed64": "number",
    "sfixed32": "number",
    "sfixed64": "number",
    "bool": "boolean",
    "string": "string",
    "bytes": "ArrayBuffer"  # 或 "Uint8Array"，取决于使用的库
}


def printDictAsKeyValue(object_: dict, currentPath_: str, printAsKVList_: list = None):
    # 删


def getReadStructTsCode(protoStructAnalyse_: ProtoStructAnalyse, protoName_: str):
    _root = dict()
    getReadDictByTableInfo(protoStructAnalyse_, _root, protoStructAnalyse_._tableFullNameDict[protoName_])
    _printAsKVList = printDictAsKeyValue(_root, protoName_)
    return "\n".join(_printAsKVList)


def getReadDictByTableInfo(protoStructAnalyse_: ProtoStructAnalyse, belongToDict_: dict, tableInfo_: dict):
    _propertyList = tableInfo_["propertyList"]
    for _i in range(len(_propertyList)):
        _property = _propertyList[_i]
        _dataType = _property["dataType"]
        _needType = _property["needType"]
        _propertyName = _property["propertyName"]
        # 普通
        if protoStructAnalyse_.isNormalProperty(_dataType):
            belongToDict_[_propertyName] = _dataType
        else:
            # 字典 或 列表
            _newDict = dict()
            _dataInfoDict = protoStructAnalyse_._tableFullNameDict[_dataType]
            if _dataInfoDict["type"] == "enum":
                belongToDict_[_propertyName] = f'{_dataType}.{_dataInfoDict["propertyList"][0]["propertyName"]}'
            else:
                getReadDictByTableInfo(protoStructAnalyse_, _newDict, _dataInfoDict)
                if _needType == "repeated":
                    # 列表
                    _newList = list()
                    belongToDict_[_propertyName] = _newList
                    _newList.append(_newDict)
                else:
                    # 字典
                    belongToDict_[_propertyName] = _newDict


# 生成创建结构
def getCreateStructTsCode(protoStructAnalyse_: ProtoStructAnalyse, structName_: str):
    _typeTableInfo = protoStructAnalyse_._tableFullNameDict[structName_]
    if _typeTableInfo is None:
        utils.printUtils.pError(f'{structName_} 不存在')
    _protoName = _typeTableInfo["fileName"].replace(".proto", "_pb")
    _codeStrList = [f"let {structName_} = {_protoName}.{structName_}.create({{"]
    getCreateDictByTableInfo(protoStructAnalyse_, _codeStrList, _typeTableInfo)
    _codeStrList.append("})")
    _tsCodeStr = "\n".join(_codeStrList)
    from Code.app.services.CodeCreateAndFormat.TypeScriptFormatter import TypeScriptFormatter
    _tsFormatter: TypeScriptFormatter = pyServiceUtils.getSubSvrByName("Code", "CodeCreateAndFormat", "TypeScriptFormatter")
    _tsCodeStr = _tsFormatter.formatTsStr(_tsCodeStr)
    return _tsCodeStr


def getEnumCodeAndCommon(protoName_: str, dataType_: str, typeTableInfo_: dict):
    _propertyList = typeTableInfo_["propertyList"]
    _codeStr = ""
    for _i in range(len(_propertyList)):
        _property = _propertyList[_i]
        if _i == 0:
            _codeStr += f'{protoName_}.{dataType_}.{_property["propertyName"]},'
        _codeStr += f'\n// {protoName_}.{dataType_}.{_property["propertyName"]} : {_property["index"]}'
    return _codeStr


def getCreateDictByTableInfo(protoStructAnalyse_: ProtoStructAnalyse, codeStrList_: list, tableInfo_: dict, depth_: int = 0):
    # 删