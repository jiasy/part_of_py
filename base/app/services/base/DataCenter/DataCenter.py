#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
import json
from base.app.services.base.DataCenter.DataEventMgr.DataEventMgr import DataEventMgr
from typing import List
from utils import listUtils
from utils import pyUtils


# dataSet 不是 jsonDict ，因为其中的list转换成了键值对

class DataCenter(BaseService):

    def __init__(self, sm_):
        super().__init__(sm_)
        self.dataSet: dict = dict({})
        self.ds: dict = self.dataSet
        self.dataEventMgr: DataEventMgr = DataEventMgr(self.sm)

    def create(self):
        self.sm.dc = self
        super(DataCenter, self).create()
        self.dataEventMgr.create()

    def destroy(self):
        self.dataEventMgr.destroy()
        self.dataEventMgr = None
        super(DataCenter, self).destroy()
        self.sm.dc = None

    # ---------------------------------其他 ---------------------------------
    def setValueToDataPath(self, dataPath_: str, value_, dataSet_: dict = None):
        # 删

    def deleteValueByDataPath(self,
                              dataPath_: str,
                              dataSet_: dict = None
                              ):
        # 删

    # 获取路径数据
    def getValueByDataPath(self,
                           dataPath_: str,
                           dataSet_: dict = None
                           ):
        # 删

    # deal with data path with array index.

    def dealKey(self, key_: str):
       #删

    # 遍历字段，提醒数据路径的监听者改变数据
    def recursiveDataPath(self,
                          dataOnParentPath_: dict,
                          valueDict_: dict,
                          dataPath_: str,
                          changeList_: list
                          ):
        # 删

    # 递归设置数据
    def resetlistOnDataPath(self,
                            dataOnCurrentDataPath_: dict,
                            dataPath_: str,
                            lastKey_: str,
                            arrayValue_: list,
                            changeList_: list
                            ):
        # 删

    def printData(self, dataSet_: dict, currentPath_: str):
        _printAsKVList = self.getPrintAsKVList(dataSet_, currentPath_)
        for _i in range(len(_printAsKVList)):
            _printAsKVStr = _printAsKVList[_i]
            print(_printAsKVStr)

    def getPrintAsKVList(self, dataSet_: dict, currentPath_: str, printAsKVList_: list = None):
        # 删

    # 简单写，因为经常使用所以写的短一些
    def gv(self, dataPath_: str, dataSet_: dict = None):
        # 通过数据路径获取数据
        return self.getValueByDataPath(dataPath_, dataSet_)

    # 删除对应路径的数据
    def dv(self, dataPath_: str, dataSet_: dict = None):
        return self.deleteValueByDataPath(dataPath_, dataSet_)

    # 给数据路径设置数据
    def sv(self, dataPath_: str, value_, dataSet_: dict = None):
        return self.setValueToDataPath(dataPath_, value_, dataSet_)

    # 将数据key排序，然后，获取排序后的Value构成的list
    def gvDictAsList(self, dataPath_: str, dataSet_: dict = None):
        _dataObject = self.gv(dataPath_, dataSet_)
        _keySortedValueArr = listUtils.getDictValueAsList(_dataObject)
        return _keySortedValueArr

    # dataSet 转换回 jsonDict
    def dataSetToJsonDict(self, dataPath_: str, dataSet_: dict = None):
        _dataSetOnPath = self.getValueByDataPath(dataPath_, dataSet_)
        _jsonDict = {}
        self.dataSetDictToJsonDict(_dataSetOnPath, _jsonDict)
        return _jsonDict

    # dataSet的每一个节点转换
    def dataSetDictToJsonDict(self, dataSetDict_: dict, jsonDict_: dict):
        # 删

    # 获取列表元素
    def getListElementByIdx(self, listDataPath_: str, idx_: int, dataSet_: dict = None):
        if self.isDataPathExist(listDataPath_ + "[0]", dataSet_):
            _listLength: int = self.getValueByDataPath(listDataPath_, dataSet_)
            if not _listLength is None:
                if idx_ < _listLength:
                    _propertyNameOfIdx = listDataPath_ + "[" + str(idx_ + 1) + "]"
                    return self.getValueByDataPath(_propertyNameOfIdx, dataSet_)
                else:
                    self.raiseError(
                        pyUtils.getCurrentRunningFunctionName(),
                        "数组索引越界 _idx ： " + str(idx_) + " ，_listLength : " + str(_listLength)
                    )
            else:
                return None
        else:
            return None

    def printDataSetJsonString(self):
        print("dataSet = " + json.dumps(self.dataSet, indent=4, sort_keys=False, ensure_ascii=False))

    def printDataSet(self):
        self.printData(self.dataSet, "")

    def dataPathValidation(self, dataPath_: str):
        if dataPath_.find("..") >= 0:
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), "数据路径不能包含..")
            return False
        elif dataPath_.find("\n") >= 0 or dataPath_.find("\r") >= 0:
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), "数据路径不能包含 换行")
            return False
        return True

    def isDataPathExist(self, dataPath_: str, dataSet_: dict = None):
        if self.dataPathValidation(dataPath_) is None:
            return False
        _dataObject = self.getValueByDataPath(dataPath_, dataSet_)
        if _dataObject is None:
            return False
        return True
