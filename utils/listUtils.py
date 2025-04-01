#!/usr/bin/env python3
import numpy as np
import math


# 模拟shift
def list_shift(list_: list, count_: int = 1):
    if count_ == 1:
        return list_.pop(0)
    else:
        _popList = []
        while count_ > 0:
            _popList.append(list_.pop(0))
            count_ = count_ - 1
        return _popList


# 模拟pop
def list_pop(list_):
    return list_.pop(len(list_) - 1)


def list_reverse(list_):
    return list_[::-1]


'''
# test
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
part1, part2, part3 = listUtils.listSplit(lst, 3, 7)
Part 1: [0, 1, 2]
Part 2: [3, 4, 5, 6, 7]
Part 3: [8, 9]
'''


# 使用指定序号拆分数据
def listSplit(lst, index1, index2):
    part1 = lst[:index1]
    part2 = lst[index1:index2 + 1]
    part3 = lst[index2 + 1:]
    return part1, part2, part3


def getDictValueAsList(dict_: dict):
    return [_value for _, _value in dict_.items()]


# 将二维数组内的行数压缩到给定值以下，采用取平均值的方式合并等分后的行
def averageListTo(list_: list, length_: int):
    if len(list_) <= length_:
        return list_
    # 向上取整， 10001 行 压缩到 10000 行以下，也就是 5000 行，不会还是 10001行。
    _averageLegth = math.ceil(len(list_) / length_)
    _backList = []
    _tempAverageList = []
    _columnLength = len(list_[0])  # 列数
    for _idx in range(len(list_)):
        _lineList = list_[_idx]
        _tempAverageList.append(_lineList)
        if _idx % _averageLegth == 0:
            _averaged_list = []
            for _columnIdx in range(0, _columnLength):  # 遍历每一列
                _columnAverage = 0
                for _lineIdx in range(len(_tempAverageList)):  # 将每行中的当前列累加后平均
                    _columnAverage += _tempAverageList[_lineIdx][_columnIdx]
                _columnAverage = _columnAverage / _columnLength
                _averaged_list.append(_columnAverage)  # 记录平均后的这一列
            _backList.append(_averaged_list)  # 记录到返回数组
            _tempAverageList = []
    return _backList


'''
_sourceStrList = [
    "+ - - * / // ** %"
    ,
    "np.add np.subtract np.negative np.multiply np.divide np.floor_divide np.power np.mod"
    ,
    "加法运算(即1+1=2) 减法运算(即3-2=1) 负数运算(即-2) 乘法运算(即2*3=6) 除法运算(即3/2=1.5) 地板除法运算(ﬂoor，division，即3//2=1) 指数运算(即2**3=8) 模/余数(即9%4=1)"
]
_list = [_str.split(" ") for _str in _sourceStrList]
_list = listUtils.transpose(_list)
for _strList in _list:
    print(_strList[0].ljust(5) + " " + _strList[1].ljust(15) + " " + _strList[2])
'''


# 二维数组转置
def transpose(list_: list):
    _columnLength = len(list_[0])
    _lineLength = len(list_)
    _targetList = []
    for _idx in range(0, _columnLength):
        _columnList = []
        for _idxLoop in range(0, _lineLength):
            _columnList.append(list_[_idxLoop][_idx])
        _targetList.append(_columnList)
    return _targetList


# 利用np进行数组转置，指定类型为 O，代表元素为Python对象。<对象的转置，反而没有以上的实现快>
def npTranspose(list_: list):
    _list = np.array(list_, dtype="O")
    return _list.T


# 字典对象构成的列表，按照对象的某一个key进行排序，默认升序
def sortListOfDict(list_: list, sortKey_: str, reverse_: bool = False):
    # 排序的结果非期望的时候，查证一下key对应的是不是数字
    list_.sort(key=lambda _info: _info.get(sortKey_), reverse=reverse_)


# 两个列表去重合并
def unionTwoList(listA_: list, listB_: list):
    return list(set(listA_).union(set(listB_)))


# 填充元素两个数组保持相同大小
def fillUnitlLenEqual(listA_: list, listB_: list, default_):
    _lengthA = len(listA_)
    _lengthB = len(listB_)
    if _lengthA > _lengthB:
        fillUnitlLen(listB_, _lengthA, default_)
    elif _lengthB > _lengthA:
        fillUnitlLen(listA_, _lengthB, default_)


# 填充数组直至给定大小
def fillUnitlLen(list_: list, targetLength_: int, default_):
    while (len(list_) < targetLength_):
        list_.append(default_)


# 将每个元素链接起来，形成字符串
def joinToStr(list_: list, joinStr_: str):
    return joinStr_.join(list_)


# 打印列表
def printList(list_: list, title_: str = "", prefix_: str = ""):
    _printStr = title_
    _strList = []
    for _idx in range(len(list_)):
        _strList.append(str(prefix_ + list_[_idx]))
    print(_printStr + "\n".join(_strList))


# 打印字典构成的列表
def printDictList(list_: list, strformat_: str, keys_: list):
    for _i in range(len(list_)):
        _dict = list_[_i]
        _valueList = []
        for _iKey in range(len(keys_)):
            _valueList.append(_dict[keys_[_iKey]])
        # SAMPLE - string format 列表做参数
        print(strformat_.format(*_valueList))


# 获取最大值
def maxInList(list_: list):
    _max = -float("inf")
    for _i in range(len(list_)):
        _current = float(list_[_i])
        if _current > _max:
            _max = _current
    return _max


# 获取最小值
def minInList(list_: list):
    _min = float("inf")
    for _i in range(len(list_)):
        _current = float(list_[_i])
        if _current < _min:
            _min = _current
    return _min


# 找到并移除
def findAndRemove(list_: list, element_):
    if element_ in list_:
        list_.pop(list_.index(element_))
        return True
    else:
        return False
