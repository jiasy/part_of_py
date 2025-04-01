import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import functools
import os
from utils import listUtils

colorList = [
    "blue", "cyan", "gray", "olive",
    "green", "indigo", "red", "darkred",
    "purple", "pink", "yellow", "brown",
    "orchid", "tomato", "orange", "chocolate",
    "peachpuff", "plum", "khaki", "cornsilk",
    "lightsteelblue", "darkgoldenrod", "darkviolet", "navy",
    "crimson", "thistle", "salmon", "deepskyblue",
    "gold", "hotpink", "peru", "maroon",
]


def getBottom(bottom_: list, memList_: list):
    _newBottom = []
    for _i in range(len(bottom_)):
        _newBottom.append(bottom_[_i] + memList_[_i])
    return _newBottom


'''
{
    "a":[1,2,3,4,5,6],
    "b":[1,2,3,4,5,6],
}
'''


def draw(infoDict_: dict, picId_: int = 1):
    plt.figure(picId_)
    picId_ = picId_ + 1

    _frameCount = 0
    for _key in infoDict_:
        _frameCount = len(infoDict_[_key])
    _x = np.arange(_frameCount)  # x 轴
    _bottomList = []  # 底
    for _i in range(_frameCount):
        _bottomList.append(0)

    _colorIdx = 0
    for _key in infoDict_:
        _frameList = len(infoDict_[_key])
        plt.bar(
            _x, _frameList, bottom=_bottomList, width=1, fc=colorList[_colorIdx],
            label=_key
        )
        _bottomList = getBottom(_bottomList, _frameList)  # 叠加底
        _colorIdx = _colorIdx + 1

    return picId_

    # 没有超过10MB的其他内存总和
    _smallMbList = []
    for _i in range(len(_totalMbList)):
        _smallMbList.append(_totalMbList[_i] - _bottomList[_i])
    plt.bar(_x, _smallMbList, bottom=_bottomList, width=1, fc=colorList[_colorIdx], label="small")

    # 图片宽高（单位是100像素）
    plt.gcf().set_size_inches(20, 10)
    # x轴每多少放置一个标
    x_major_locator = MultipleLocator(50)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    # 标题
    plt.title("TOTAL")
    # 轴上起止坐标
    plt.ylim(0, _maxMB * 1.1)  # y 轴放大1.1，上方有点儿空间
    plt.xlim(0, len(_totalMbList))  # x轴按照个数做起止坐标
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(picFolder_, "TOTAL.png"))
