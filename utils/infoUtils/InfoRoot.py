from utils.infoUtils.InfoGroup import InfoGroup
from utils.infoUtils.InfoType import InfoType
import os.path
import sys
from colorama import init
from utils import excelControlUtils
from xlwings.base_classes import Sheet
from xlwings.base_classes import Book

_isInited = False


# 日志类
class InfoRoot:
    # _instance = None
    # _initialized = None
    #
    # # SAMPLE 单子类
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super().__new__(cls, *args, **kwargs)
    #     return cls._instance
    #
    # def __init__(self, type_: Type = Type.Color):
    #     if not self._initialized:
    #         self._initialized = True
    #     else:
    #         return
    #     self.type = type_
    #     self.infoGroupList: list[InfoGroup] = []

    def __init__(self, type_: InfoType = InfoType.Color):
        self.type = type_
        self.infoGroupList: list[InfoGroup] = []

    # 清理
    def clear(self):
        self.infoGroupList = []

    def addLine(self):
        return self.newLine()

    # 添加新的一行，是否添加一个新组
    def newLine(self, startNewGroup: bool = False):
        if startNewGroup is False:  # 不需要开新组
            if len(self.infoGroupList) == 0:  # 没组，默认加一个
                self.addGroup()
        else:  # 开新组
            self.addGroup()
        return self.infoGroupList[-1].newLine()  # 最后一个组添新行

    # 向指定的id添加一行并返回
    def addLineToGroup(self, id_: int = None):
        _group = self.getOrAddGroup(id_)
        if _group is None:
            return None
        return _group.newLine()  # 最后一个组添新行

    # 有 id_ 的时候为获取，没有时为添加一个
    def getOrAddGroup(self, id_: int = None):
        if id_ is None:  # 不指定的话
            return self.addGroup()
        else:
            if id_ <= len(self.infoGroupList):  # id_ 在范围内
                return self.infoGroupList[id_ - 1]  # 返回指定的
            elif id_ == len(self.infoGroupList) + 1:
                return self.addGroup()
            else:
                return None

    def addGroup(self):
        self.infoGroupList.append(InfoGroup(len(self.infoGroupList) + 1, self))  # 添加到最后
        return self.infoGroupList[-1]  # 返回最后的这个

    def doPrint(self, targetType_: InfoType = None, targetExcelPath_: str = None):
        if targetType_ is None:
            targetType_ = self.type

        if targetType_ == InfoType.Color:
            # 初始化
            global _isInited
            if _isInited is False:
                init(autoreset=True)
                _isInited = True
            _printStr = ""
            for _i in range(len(self.infoGroupList)):  # 遍历组
                _printStr = _printStr + self.infoGroupList[_i].doPrint(targetType_)
            print(_printStr)
        elif targetType_ == InfoType.ExcelShape or targetType_ == InfoType.ExcelCell:
            _workBook: Book = excelControlUtils.openExclWorkBook(targetExcelPath_)
            # 不同的 Sheet 写入方式
            _oneSheet = True
            # if targetType_ == InfoType.ExcelShape:
            #     _oneSheet = False
            # elif targetType_ == InfoType.ExcelCell:
            #     _oneSheet = True
            if _oneSheet:  # 全写到一个Sheet中
                _sheet: Sheet = excelControlUtils.addDefaultSheet(_workBook)  # 添加一个默认的sheet
                _curHeightOrRowCount = 0  # 当前的高度（Shape时）、当前的行数（Cell时）
                for _i in range(len(self.infoGroupList)):  # 遍历组
                    _curHeightOrRowCount = self.infoGroupList[_i].doPrint(targetType_, targetExcelPath_, _sheet, _curHeightOrRowCount)  # 写入 sheet,更新高度
            else:  # 写到多个Sheet中
                for _i in range(len(self.infoGroupList)):  # 遍历组
                    _infoGroup = self.infoGroupList[_i]
                    _sheet: Sheet = excelControlUtils.addDefaultSheet(_workBook)  # 添加一个默认的sheet
                    _infoGroup.doPrint(targetType_, targetExcelPath_, _sheet, 0)  # 写入 sheet
        return self
