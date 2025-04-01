from utils.infoUtils.InfoLine import InfoLine
from utils.infoUtils.InfoType import InfoType
from utils import excelControlUtils
from xlwings.base_classes import Sheet


class InfoGroup:
    def __init__(self, id_: int, infoRoot_):
        self.infoLineList: list[InfoLine] = []
        self.infoRoot = infoRoot_
        self.sheetName = f"Gp_{id_}"

    def addLine(self, infoLine_: InfoLine):
        self.infoLineList.append(infoLine_)

    def newLine(self):
        _newLine = InfoLine(self.infoRoot)  # 最后一个组添新行
        self.addLine(_newLine)
        return _newLine

    def doPrint(self, targetType_: InfoType = None, targetExcelPath_: str = None, targetSheet_: Sheet = None, curHeightOrRow_: int = 0):
        if targetType_ is None:
            targetType_ = self.infoRoot.type
        if targetType_ == InfoType.Color:
            _printStr = ""
            for _iLoop in range(len(self.infoLineList)):  # 遍历组的每一行
                _infoLine = self.infoLineList[_iLoop]
                _printStr = _printStr + _infoLine.getPrint(targetType_)
                if _iLoop != len(self.infoLineList) - 1:  # 不是最后一个需要补充回车
                    _printStr = _printStr + "\n"
            return _printStr
        elif targetType_ == InfoType.ExcelShape:
            _paramStr = self.getExcelParamStr(targetType_, 10, curHeightOrRow_, 12)  # 获取 Excel 参数
            curHeightOrRow_ = excelControlUtils.createTextRectTangle(targetExcelPath_, targetSheet_, _paramStr)
            return curHeightOrRow_ + 10
        elif targetType_ == InfoType.ExcelCell:
            if curHeightOrRow_ == 0:
                curHeightOrRow_ = 1  # 作为格子坐标，不可能为0
            _paramStr = self.getExcelParamStr(targetType_, 1, curHeightOrRow_, 7)  # 获取 Excel 参数
            excelControlUtils.writeAndMergeCell(targetExcelPath_, targetSheet_, _paramStr)
            return curHeightOrRow_ + len(self.infoLineList) + 1

    # xPos_，yPos_ 为 当前 shape 的起始位置 或 当前 Cell 的位置
    # paramNum_ 为 Segment 的 参数个数
    def getExcelParamStr(self, targetType_: InfoType, xPos_: int, yPos_: int, paramNum_: int):
        _paramStr = f"{xPos_}&{yPos_}&{paramNum_}&{255}&{255}&{255}&&"  # 第一行，当前高，背景色
        for _i in range(len(self.infoLineList)):  # 遍历组的每一行
            _infoLine = self.infoLineList[_i]
            _paramsList = _infoLine.getPrint(targetType_)  # 获取要打印的参数
            for _iLoop in range(len(_paramsList)):  # 每一段
                _params = _paramsList[_iLoop]  # 每一段的参数
                for _iLoopStr in range(len(_params)):
                    _paramStr = _paramStr + f'{_params[_iLoopStr]}'
                    if _iLoopStr != (len(_params) - 1):
                        _paramStr = f'{_paramStr}&'  # 不是最后的需要加链接符
                if _iLoop != (len(_paramsList) - 1):
                    _paramStr = f'{_paramStr}&'  # 不是最后的需要加链接符
            if _i != (len(self.infoLineList) - 1):
                _paramStr = f'{_paramStr}&&'  # 下一行需要再加 &&
        return _paramStr
