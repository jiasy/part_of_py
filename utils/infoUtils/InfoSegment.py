from utils.infoUtils.InfoColor import InfoColor
from utils.infoUtils.InfoType import InfoType
from termcolor import colored


class InfoSegment:
    def __init__(self, logStr_: str, infoRoot_, frontColor_: InfoColor = None, bgColor_: InfoColor = None, attrList_: list = None):
        self.logStr = logStr_
        self.frontColor = frontColor_
        self.bgColor = bgColor_
        self.attrList = attrList_
        self.infoRoot = infoRoot_

    def getPrint(self, targetType_: InfoType = None):
        if targetType_ is None:
            targetType_ = self.infoRoot.type
        if targetType_ == InfoType.Color:
            if self.frontColor is not None:
                if self.bgColor is not None:
                    if self.attrList is not None:
                        return colored(self.logStr, self.frontColor.value, f"on_{self.bgColor.value}", attrs=self.attrList)
                    else:
                        return colored(self.logStr, self.frontColor.value, f"on_{self.bgColor.value}")
                else:
                    return colored(self.logStr, self.frontColor.value, attrs=self.attrList)
            else:
                return self.logStr
        elif targetType_ == InfoType.ExcelShape:
            if '&' in self.logStr:
                print(f"ERROR : {self.logStr} 有 &")
            _fontColor = InfoColor.getColorRgbByType(self.frontColor)  # 字色
            _fontSize = 20  # 字号
            _bgColor = InfoColor.getColorRgbByType(self.bgColor)  # 背景色
            _lineWidth = 0  # 线宽
            _lineColor = 0, 0, 0  # 线色
            return [_fontColor[0], _fontColor[1], _fontColor[2], _bgColor[0], _bgColor[1], _bgColor[2], _lineColor[0], _lineColor[1], _lineColor[2], _fontSize, _lineWidth, self.logStr]
        elif targetType_ == InfoType.ExcelCell:
            if '&' in self.logStr:
                print(f"ERROR : {self.logStr} 有 &")
            _fontColor = InfoColor.getColorRgbByType(self.frontColor)  # 字色
            _bgColor = InfoColor.getColorRgbByType(self.bgColor)  # 背景色
            return [_fontColor[0], _fontColor[1], _fontColor[2], _bgColor[0], _bgColor[1], _bgColor[2], self.logStr]


if __name__ == "__main__":
    from utils.infoUtils.InfoRoot import InfoRoot
    from utils.infoUtils.InfoLine import InfoLine
    from utils.infoUtils.InfoType import InfoType

    _infoRoot = InfoRoot()
    _infoLine: InfoLine = _infoRoot.addLine()
    _infoLine.addInfo("一二三四五六七八九十", InfoColor.Yellow, InfoColor.Black)
    _infoRoot.doPrint(InfoType.ExcelCell, "/Users/nobody/Downloads/rar/PythonExcel/Guide_Desc.xlsx")
