import logging
import sys
import re

import utils.printUtils
from utils import strUtils


def analyseLine(line_: str):
    # 删


def getModuleAndFunc(str_: str):
    _proto_module, _proto_func = strUtils.splitToAB(str_, ".")
    if _proto_module == None:
        _proto_module, _proto_func, _temp = strUtils.splitToABC(str_, ".")
        _proto_module = _proto_module + "." + _proto_func
        _proto_func = _temp
        if _proto_module == None:
            utils.printUtils.pError(str_ + " 无法用 . 分割")
            sys.exit(1)
    return _proto_module, _proto_func


# 从字典中取得对象
def getProtoTable(protoInfoDict_: dict, protoName_: str):
    _tableList = protoInfoDict_["tableList"]  # 字段列表
    for _i in range(len(_tableList)):
        _table = _tableList[_i]
        if protoName_ == _table["protoName"]:  # 字段名
            return _table
    utils.printUtils.pError(protoInfoDict_["fileName"] + " 不存在 " + str(protoName_) + " 的结构指定")
    sys.exit(1)


def getArgsStr(protoTable_):
    _backStr = ""
    _protoPropertyList = protoTable_["propertyList"]
    _length = len(_protoPropertyList)
    for _idx in range(_length):
        _propertyName = _protoPropertyList[_idx]["propertyName"]
        _backStr = _backStr + _propertyName + " : " + _propertyName
        if _idx != (_length - 1):
            _backStr = _backStr + ","
    return "{" + _backStr + "}"
