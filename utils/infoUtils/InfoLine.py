from utils.infoUtils.InfoSegment import InfoSegment
from utils.infoUtils.InfoColor import InfoColor
from utils.infoUtils.InfoBlank import InfoBlank
from utils.infoUtils.InfoType import InfoType


# 一行日志
class InfoLine:
    def __init__(self, infoRoot_):
        self.infoSegmentList: list[InfoSegment] = []
        self.infoRoot = infoRoot_

    def addInfo(self, logStr_: str, frontColor_: InfoColor = None, bgColor_: InfoColor = None, attrList_: list = None):
        self.infoSegmentList.append(InfoSegment(logStr_, self.infoRoot, frontColor_, bgColor_, attrList_))
        return self

    # 添加一个空白
    def addBlank(self, color_: InfoColor = None):
        if color_ is None:
            self.infoSegmentList.append(InfoBlank(self.infoRoot))
        else:
            self.infoSegmentList.append(InfoSegment("  ", self.infoRoot, InfoColor.Grey, color_))
        return self

    def getPrint(self, targetType_: InfoType = None):
        if targetType_ is None:
            targetType_ = self.infoRoot.type
        if targetType_ == InfoType.Color:
            _printStr = ""
            for _i in range(len(self.infoSegmentList)):
                _infoSegment = self.infoSegmentList[_i]
                _printStr = _printStr + _infoSegment.getPrint(targetType_)
            return _printStr
        elif targetType_ == InfoType.ExcelShape or targetType_ == InfoType.ExcelCell:
            _paramsList = []
            for _i in range(len(self.infoSegmentList)):
                _infoSegment = self.infoSegmentList[_i]
                _paramsList.append(_infoSegment.getPrint(targetType_))  # 获取参数
            return _paramsList
