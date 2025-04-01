#!/usr/bin/env python3
# Created by nobody at 2023/7/18
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import xmlUtils


class FontFix(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.scaleKeyValueDict = None
        self.textId = None
        self.gearSizeDict = None
        self.gearFontSizeDict = None

    def create(self):
        super(FontFix, self).create()

    def destroy(self):
        super(FontFix, self).destroy()

    # def fixScaleInfo(self, xmlPath_: str, textDict_: dict):

    def getScaleControllerDict(self, xmlPath_: str, xmlContentDict_: dict):
        _scaleInfoDict = None  # 描述大小的控制器
        if "controller" in xmlContentDict_["component"]:
            _controllerList = xmlContentDict_["component"]["controller"]
            if _controllerList is list or "@name" not in _controllerList:
                for _idxLoop in range(len(_controllerList)):
                    _scaleInfoDict = self.getScaleController(_controllerList[_idxLoop])
                    if _scaleInfoDict is not None:
                        break
            else:
                _scaleInfoDict = self.getScaleController(_controllerList)
        if _scaleInfoDict is not None:
            _pageInfoStr = _scaleInfoDict["@pages"]  # '0,100,1,45,2,30'
            _pageInfoList = _pageInfoStr.split(",")
            _backScaleKeyValueDict = {}  # { 0:100 , 2:30 }
            for _i in range(len(_pageInfoList)):
                if _i % 2 == 0:
                    _key = _pageInfoList[_i]
                    _value = _pageInfoList[_i + 1]
                    _backScaleKeyValueDict[_key] = _value
            if "0" not in _backScaleKeyValueDict:
                print(f"ERROR : {xmlPath_} scale 作为控制器，没有 0 键")
            if _backScaleKeyValueDict["0"] != "100":
                print(f"ERROR : {xmlPath_} scale 作为控制器，0一定为100")
            return _backScaleKeyValueDict
        else:
            return None

    def getScaleController(self, controllerDict_: dict):
        if controllerDict_["@name"] == "scale":
            return controllerDict_
        return None

    # 修改指定文本
    def fixText(self, textDict: dict):
        if self.textId is None or self.gearSizeDict is None or self.gearFontSizeDict is None:
            utils.printUtils.pError("ERROR : 缺少 可用 值")
            sys.exit(1)
        if textDict["@id"] == self.textId:  # 查到指定文本
            textDict["gearSize"] = self.gearSizeDict  # 新增 或 覆盖 掉
            textDict["gearFontSize"] = self.gearFontSizeDict
            return textDict
        return None

    def fixScaleInfo(self, xmlPath_: str, textDict_: dict):
        print(textDict_)
        self.textId = textDict_["@id"]
        # default 宽高、大小、字体大小
        _defaultWidth, _defaultHeight, _defaultScaleX, _defaultScaleY, _defaultFontSize = None, None, 1, 1, None
        # 有 gear 指定时，取 gear 的 default
        if "gearSize" in textDict_:
            _defaultWidth, _defaultHeight, _defaultScaleX, _defaultScaleY = str(textDict_["gearSize"]["@default"]).split(",")
        else:
            _defaultWidth, _defaultHeight = str(textDict_["@size"]).split(",")
            if "@scale" in textDict_:
                _defaultWidth, _defaultHeight = str(textDict_["@scale"]).split(",")
        _defaultWidth = int(_defaultWidth)
        _defaultHeight = int(_defaultHeight)
        _defaultScaleX = float(_defaultScaleX)
        _defaultScaleY = float(_defaultScaleY)
        if "gearFontSize" in textDict_:
            _defaultFontSize = str(textDict_["gearFontSize"]["@default"])
        else:
            _defaultFontSize = textDict_["@fontSize"]
        _defaultFontSize = int(_defaultFontSize)
        # 生成新的 gearSize
        _pagesList = []
        _sizeList = []
        _fontSizeList = []
        _defaultSizeStr = None
        _defaultFontSizeStr = None
        for _keyStr in self.scaleKeyValueDict:
            _valueStr = self.scaleKeyValueDict[_keyStr]
            _value = float(int(_valueStr) / 100.0)
            if _keyStr != "0":
                _pagesList.append(_keyStr)  # 非默认值全部重新计算大小
                _sizeList.append(f"{int(_defaultWidth / _value)},{int(_defaultHeight / _value)},{_defaultScaleX * _value:.2f},{_defaultScaleY * _value:.2f}")
                _fontSizeList.append(f"{int(_defaultFontSize / _value)}")
            else:
                _defaultSizeStr = f"{_defaultWidth},{_defaultHeight},{_defaultScaleX},{_defaultScaleY}"
                _defaultFontSizeStr = f"{_defaultFontSize}"
        # 拼接 文本大小适配
        self.gearSizeDict = {
            "@controller": "scale",
            "@pages": "|".join(_pagesList),
            "@values": "|".join(_sizeList),
            "@default": _defaultSizeStr
        }
        self.gearFontSizeDict = {
            "@controller": "scale",
            "@pages": "|".join(_pagesList),
            "@values": "|".join(_fontSizeList),
            "@default": _defaultFontSizeStr
        }
        xmlUtils.replaceXmlLine(xmlPath_, "text", "text", self.fixText)
        self.textId = None
        self.gearSizeDict = None
        self.gearFontSizeDict = None

    def fixScale(self, xmlPath_: str, xmlContentDict_: dict):
        # 先取得当前 scale 控制器的键值信息
        self.scaleKeyValueDict = self.getScaleControllerDict(xmlPath_, xmlContentDict_)
        # 有大小指定，重新生成一遍，字体大小和文本框大小
        if self.scaleKeyValueDict is not None:
            if "text" in xmlContentDict_["component"]["displayList"]:
                _textList = xmlContentDict_["component"]["displayList"]["text"]
                if _textList is list or "@id" not in _textList:
                    for _idxLoop in range(len(_textList)):
                        self.fixScaleInfo(xmlPath_, _textList[_idxLoop])
                else:
                    self.fixScaleInfo(xmlPath_, _textList)


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils
    import os

    # 当添加了 scale 控制器之后，所有的 text 需要按照 scale 进行一次大小和字体的调整
    _xmlPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets/HeroesHall/HeroesHallRecruitItem.xml")
    _xmlDict = xmlUtils.xmlDictFromFile(_xmlPath)
    _subSvr.fixScale(_xmlPath, _xmlDict)
