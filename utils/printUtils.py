# !/usr/bin/env python3
import json
from utils import dictUtils
from utils.infoUtils.InfoColor import InfoColor
from utils.infoUtils.InfoRoot import InfoRoot
from utils.infoUtils.InfoType import InfoType
from utils.pyUtils import AppError

infoIns: InfoRoot = None

def printPropertys(object_):
    print("propertys : " + str(object_.__dict__))


def printList(list_: list, prefix_: str = ""):
    _length: int = len(list_)
    _blankCount: int = 0
    if _length < 10:
        _blankCount = 1
    elif _length > 9999:
        _blankCount = 5
    elif _length > 999:
        _blankCount = 4
    elif _length > 99:
        _blankCount = 3
    elif _length > 9:
        _blankCount = 2
    else:
        raise AppError("万行以上？")

    for _idx in range(_length):
        _key = str(_idx).rjust(_blankCount)
        _value = str(list_[_idx])
        _printStr = f'{prefix_}{_key} : {_value}'
        pLog(_printStr)


# 转str，转json，转对象，在打印成键值对
def printPyObjAsKV(prefix_: str, obj_: dict, showType_: bool = False):
    print(prefix_ + " ---------------------------------------------")
    _printStr = str(obj_).replace("\'", "\"").replace("True", "true").replace("False", "false").replace("None", "null")
    _jsonDict = json.loads(_printStr)
    dictUtils.printDictAsKeyValue(_jsonDict, prefix_, showType_)
    print()


def printDictStruct(dictName_: str, dict_: dict, depth_: int = 0):
    print("|      " * depth_ + "+--" + dictName_)
    dictUtils.showDictStructure(dict_, depth_ + 1)


def getInfoIns():
    global infoIns
    if infoIns is None:
        infoIns = InfoRoot(InfoType.Color)
    return infoIns


# prefixColorList_ 前置的缩进颜色
def pLogInside(logStr_: str, title_: str, logFontColor_: InfoColor, titleFontColor_: InfoColor = None, prefixColorList_: list[InfoColor] = None):
    _infoIns: InfoRoot = getInfoIns()
    _newLine = _infoIns.addLine()
    # 前置 颜色
    if prefixColorList_ is not None:
        for _i in range(len(prefixColorList_)):
            _prefixColor = prefixColorList_[_i]
            _newLine.addInfo(" ", _prefixColor, _prefixColor)
    if title_ is not None:
        _newLine.addInfo(title_, titleFontColor_, logFontColor_)
    _newLine.addInfo(logStr_, logFontColor_)
    _infoIns.doPrint().clear()


def pLog(logStr_: str, prefixColorList_: list[InfoColor] = None):
    pLogInside(str(logStr_), None, InfoColor.Blue, None, prefixColorList_)


def pWarn(logStr_: str, prefixColorList_: list[InfoColor] = None):
    pLogInside(str(logStr_), None, InfoColor.Yellow, None, prefixColorList_)


def pError(logStr_: str, prefixColorList_: list[InfoColor] = None):
    pLogInside(str(logStr_), None, InfoColor.Red, None, prefixColorList_)


# 带标题的
def pTitleLog(titleStr_: str, logStr_: str, prefixColorList_: list[InfoColor] = None):
    pLogInside(f' {logStr_}', f' {titleStr_} ', InfoColor.Blue, InfoColor.Black, prefixColorList_)


def pTitleWarn(titleStr_: str, logStr_: str, prefixColorList_: list[InfoColor] = None):
    pLogInside(f' {logStr_}', f' {titleStr_} ', InfoColor.Yellow, InfoColor.Black, prefixColorList_)


def pTitleError(titleStr_: str, logStr_: str, prefixColorList_: list[InfoColor] = None):
    pLogInside(f' {logStr_}', f' {titleStr_} ', InfoColor.Red, InfoColor.Black, prefixColorList_)


if __name__ == '__main__':
    pLog(1, [InfoColor.Red])
    pWarn(2, [InfoColor.Red, InfoColor.Red])
    pError(3)
    pTitleLog(1, 1)
    pTitleWarn(1, 2, [InfoColor.Blue])
    pTitleError(1, 3, [InfoColor.Blue, InfoColor.Yellow])
