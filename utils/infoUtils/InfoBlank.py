from utils.infoUtils.InfoSegment import InfoSegment
from utils.infoUtils.InfoType import InfoType
import os.path
import sys
from termcolor import colored
from colorama import init
from utils import excelControlUtils
from xlwings.base_classes import Sheet
from xlwings.base_classes import Book


class InfoBlank(InfoSegment):
    def __init__(self, infoRoot_):
        super().__init__(None, infoRoot_, None, None, None)
        return

    def getPrint(self, targetType_: InfoType = None):
        if targetType_ is None:
            targetType_ = self.infoRoot.type
        if targetType_ == InfoType.Color:
            return " "
        elif targetType_ == InfoType.ExcelShape:
            return [0, 0, 0, 38, 38, 38, 0, 0, 0, 20, 1, " "]
        elif targetType_ == InfoType.ExcelCell:
            return [0, 0, 0, 38, 38, 38, " "]
