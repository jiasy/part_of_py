from utils import pyServiceUtils

from Excel.ExcelBaseInService import ExcelBaseInService
import cv2
import os
from utils import imageUtils
from utils import folderUtils

import shutil


class PicInfo():
    def __init__(self):
        self.pic = None
        self.filePath = None
        self.width = 0
        self.height = 0
        self.makeAsRemove = False
        self.gray = None


class Rect():
    # 左上角 0,0 点
    def __init__(self, xMin_: int, yMin_: int, xMax_: int, yMax_: int):
        self.xMin = xMin_
        self.yMin = yMin_
        self.xMax = xMax_
        self.yMax = yMax_
        self.area = (self.xMax - self.xMin) * (self.yMax - self.yMin)

    def crossArr(self, other_):
        if (self.xMax <= other_.xMin or other_.yMax <= self.xMin) and \
                (self.yMax <= other_.yMin or other_.yMax <= self.yMin):
            return 0
        else:
            _height = min(self.yMax, other_.yMax) - max(self.yMin, other_.yMin)
            _width = min(self.xMax, other_.xMax) - max(self.xMin, other_.xMin)
            _crossArea = _height * _width
            if _crossArea < 0:
                return 0
            else:
                _crossPercent = (_crossArea / self.area)
                print('_crossPercent = ' + str(_crossPercent))
                return _crossPercent

    def printSelf(self):
        print('min(' + str(self.xMin) + "," + str(self.yMin) + ")")
        print('max(' + str(self.xMax) + "," + str(self.yMax) + ")")


methodList = [
    cv2.TM_SQDIFF_NORMED,  # （归一化平方差匹配法）
    cv2.TM_CCORR_NORMED,  # （归一化相关匹配法）
    cv2.TM_CCOEFF_NORMED,  # （归一化相关系数匹配法）
]


def showMatch(src_, template_):
    _tHeight, _tWidth = template_.shape[:2]
    _rectList = []
    for _idx in range(len(methodList)):
        _method = methodList[_idx]
        # result是我们各种算法下匹配后的图像
        _result = cv2.matchTemplate(src_, template_, _method)
        # 获取的是每种公式中计算出来的值，每个像素点都对应一个值
        _minVal, _maxVal, _minLoc, _maxLoc = cv2.minMaxLoc(_result)
        if _method == cv2.TM_SQDIFF_NORMED:
            _tLeftUp = _minLoc  # _tLeftUp是左上角点
        else:
            _tLeftUp = _maxLoc
        _bottomRight = (_tLeftUp[0] + _tWidth, _tLeftUp[1] + _tHeight)  # 右下点
        _rectList.append(Rect(_tLeftUp[0], _tLeftUp[1], _bottomRight[0], _bottomRight[1]))

    _cross01 = _rectList[0].crossArr(_rectList[1])
    _cross12 = _rectList[1].crossArr(_rectList[2])
    _cross02 = _rectList[0].crossArr(_rectList[2])

    # 任意两个算法交集 90%，正明找到了
    if _cross01 > 0.9:
        return True
    elif _cross12 > 0.9:
        return True
    elif _cross02 > 0.9:
        return True
    else:
        return False


class PixaveRecoverDelete(ExcelBaseInService):
    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(PixaveRecoverDelete, self).create()

    def destroy(self):
        super(PixaveRecoverDelete, self).destroy()

    def getPicInfoListInFolderPath(self, picFolderPath_: str):
        _picList = folderUtils.getFilterFilesInPath(picFolderPath_, [".jpg"])
        _picInfoList = []
        for _i in range(len(_picList)):
            print('_i = ' + str(_i))
            _picInfo = PicInfo()
            _picInfo.filePath = _picList[_i]
            _picInfo.pic = cv2.imread(_picInfo.filePath)  # 图中的小图
            _picInfo.pic = cv2.resize(_picInfo.pic, (0, 0), fx=1, fy=1)
            _picInfo.gray = cv2.cvtColor(_picInfo.pic, cv2.COLOR_BGR2GRAY)
            _size = _picInfo.pic.shape[:2]
            _picInfo.height = _size[0]
            _picInfo.width = _size[1]
            _picInfoList.append(_picInfo)
        return _picInfoList

    # 获取 大图 和 小图（小的在前面）。
    def getPicSrcAndTemplete(self, picInfoA_, picInfoB_):
        if picInfoA_.width >= picInfoB_.width:
            if picInfoA_.height > picInfoB_.height:
                return picInfoB_, picInfoA_, True
        if picInfoA_.height >= picInfoB_.height:
            if picInfoA_.width > picInfoB_.width:
                return picInfoB_, picInfoA_, True
        if picInfoB_.width >= picInfoA_.width:
            if picInfoB_.height > picInfoA_.height:
                return picInfoA_, picInfoB_, False
        if picInfoB_.height >= picInfoA_.height:
            if picInfoB_.width > picInfoA_.width:
                return picInfoA_, picInfoB_, False
        return None, None, None

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    _subSvr.recover(
        "/Users/nobody/Documents/picUse/contact1/",
        "/Users/nobody/Documents/picUse/contact/",
    )
