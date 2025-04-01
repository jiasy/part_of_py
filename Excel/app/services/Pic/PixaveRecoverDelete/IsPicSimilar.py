import cv2
import shutil

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


def showMatch(src_, template_):
    _methodList = [
        cv2.TM_SQDIFF_NORMED,  # （归一化平方差匹配法）
        cv2.TM_CCORR_NORMED,  # （归一化相关匹配法）
        cv2.TM_CCOEFF_NORMED,  # （归一化相关系数匹配法）
    ]
    _tHeight, _tWidth = template_.shape[:2]
    _rectList = []
    for _idx in range(len(_methodList)):
        _method = _methodList[_idx]
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
        markMatchRect(src_, " - 01 - ", _rectList[0], _rectList[1])
        _rectList[0].printSelf()
        _rectList[1].printSelf()
        return True
    elif _cross12 > 0.9:
        markMatchRect(src_, " - 12 - ", _rectList[1], _rectList[2])
        _rectList[1].printSelf()
        _rectList[2].printSelf()
        return True
    elif _cross02 > 0.9:
        markMatchRect(src_, " - 02 - ", _rectList[0], _rectList[2])
        _rectList[0].printSelf()
        _rectList[2].printSelf()
        return True
    elif _cross01 > 0.75 and _cross12 > 0.75 and _cross02 > 0.75:
        # 三个算法的交集在 75 以上，也认为找到了
        markMatchRect(src_, " - 012 - ", _rectList[0], _rectList[2])
        _rectList[0].printSelf()
        _rectList[1].printSelf()
        _rectList[2].printSelf()
        return True
    else:
        return False


def markMatchRect(src_, title_, rect1_, rect2_, rect3_=None):
    cv2.rectangle(src_, (rect1_.xMin, rect1_.yMin), (rect1_.xMax, rect1_.yMax), (0, 0, 255), 2)
    cv2.rectangle(src_, (rect2_.xMin, rect2_.yMin), (rect2_.xMax, rect2_.yMax), (255, 0, 0), 2)
    if rect3_:
        cv2.rectangle(src_, (rect3_.xMin, rect3_.yMin), (rect3_.xMax, rect3_.yMax), (0, 255, 0), 2)
    cv2.imshow(title_, src_)


if __name__ == '__main__':
    _srcPath = "/Users/nobody/Documents/picUse/contact1/IMG (326) 2.jpg"
    # _templatePath = "/Users/nobody/Documents/picUse/contact1/IMG (265) 2.jpg"
    # _templatePath = "/Users/nobody/Documents/picUse/contact1/IMG (286).jpg"
    _templatePath = "/Users/nobody/Documents/picUse/contact1/IMG (326).jpg"
    # _templatePath = "/Users/nobody/Documents/picUse/contact1/IMG (274) 2.jpg"

    # 读取图片
    _src = cv2.imread(_srcPath)
    _template = cv2.imread(_templatePath)

    cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)  # 创建GUI窗口,形式为自适应
    cv2.imshow("input image", _src)  # 通过名字将图像和窗口联系

    if showMatch(_src, _template):
        print("is match")
        shutil.move(
            _srcPath,
            "/Users/nobody/Documents/picUse/contact/" + _srcPath.split("/Users/nobody/Documents/picUse/contact1/")[1]
        )
    else:
        print("not match")

    cv2.waitKey(0)  # 等待用户操作，里面等待参数是毫秒，我们填写0，代表是永远，等待用户操作
    cv2.destroyAllWindows()  # 销毁所有窗口
