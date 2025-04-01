from enum import Enum


class IdxHelper:

    def __init__(self):
        self.idx = -1
        self.markDict = {}
        self.length = None

    def init(self, length_: int = None):
        self.idx = 1
        self.markDict = {}
        self.length = length_

    # 索引推进
    def next(self):
        if self.length == None:
            self.idx += 1
            return self.idx
        else:
            if self.idx >= self.length:
                return None
            else:
                self.idx += 1
                if self.idx >= self.length:
                    return None
                return self.idx

    # 当前的索引进行一次标记
    def mark(self, markName_: str):
        if not (markName_ in self.markDict):
            _markList = []
            self.markDict[markName_] = _markList
        else:
            _markList = self.markDict[markName_]
        # 标记当前索引
        _markList.append(self.idx)

    # 获取最后一个标记的索引
    def getLastMark(self, markName_: str):
        if not (markName_ in self.markDict):
            return None
        _markList = self.markDict[markName_]
        return _markList[-1]

    # 获取标记列表
    def getMarkList(self, markName_: str):
        if not (markName_ in self.markDict):
            return None
        return self.markDict[markName_]

    def getMarkListBetweenLastTwo(self, markName_: str):
        if not (markName_ in self.markDict):
            return None
        _markList = self.markDict[markName_]
        if len(_markList) < 2:  # 不够两个就返回
            return None
        return self.getMarkListBetween(markName_, len(_markList) - 1, len(_markList) - 2)

    # 根据标记序号，获取序号关联的索引的范围
    def getMarkListBetween(self, markName_: str, beginIdx_: int, endIdx_: int):
        '''
    1
    2 - <m 0> -
    3
    4 - <m 1> -
    5
    getMarkListBetween("x",0,1,False) -> [2,3,4]
        '''
        if not (markName_ in self.markDict):
            return None
        _markList = self.markDict[markName_]
        _tempList = []
        for _idx in range(_markList[beginIdx_], _markList[endIdx_]):  # 遍历两个序号对应的索引
            _tempList.append(_idx)
        return _tempList
