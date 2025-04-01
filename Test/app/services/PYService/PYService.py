#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from base.app.services.base.DataCenter.DataBindings.DataCompare import DataCompare
from base.app.services.base.DataCenter.DataBindings.DataConnector import DataConnector
from utils import dictUtils
import json


class PYService(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(PYService, self).create()
        self.doTest()

    def destroy(self):
        super(PYService, self).destroy()

    def doTest(self):
        _jsonStr = '{"testArr": [[1], [2]]}';
        _jsonDict = json.loads(_jsonStr)

        # 输出结构
        print('dictUtils.showDict(_jsonDict) : ----------------------------------')
        dictUtils.showDictStructure(_jsonDict)

        # 设置数据，经过转化
        _changeList = self.sm.dc.sv("user", _jsonDict)
        # 输出数据变化过的路径
        print('变更路径')
        for _i in range(len(_changeList)):
            _key = _changeList[_i]
            _value = self.sm.dc.gv(_key)
            print('[{}] {} : {}'.format(_i,_key,_value))


        # # 转化过的数据，在序列化成字符串
        # _dataSetStr = str(json.dumps(self.sm.dc.ds, indent=4, sort_keys=False, ensure_ascii=False))
        # print('_dataSetStr = \n' + str(_dataSetStr))

        # 取得没有转换的源数据
        _activityInfoListLength = self.sm.dc.gv("user.activityInfo")
        print('_activityInfoListLength = \n' + str(_activityInfoListLength))
        print('self.sm.dc.ds.activityInfo = ' + str(self.sm.dc.ds["user"]["activityInfo"]))

        # 用于数据比较的数据绑定 -----------------------------------------------------------------
        _dataCompare = DataCompare(self.sm)
        _dataCompare.create()
        print(_dataCompare.resetByStr("user.result>=1")[1])
        print(_dataCompare.resetByStr("user.result<1")[1])

        # 用于字符串显示的数据绑定 ---------------------------------------------------------------
        _dataConnector = DataConnector(self.sm)
        _dataConnector.create()
        # 数组中某一项通过字符串拼接的方式获取其中内容
        _idx = 6
        _propertyName = "user.activityInfo"
        _propertyNameOfIdx = _propertyName + "[" + str(_idx + 1) + "]"
        print(_dataConnector.resetByStr("当前的第" + str(_idx + 1) + "个活动Id:${" + _propertyNameOfIdx + ".id}")[1])
        # 以某一个层级获取到的数据对象为起始点，通过 相对数据路径 取 数据
        _activityDict = self.sm.dc.getListElementByIdx("user.activityInfo", _idx)
        _startTime_low = self.sm.dc.gv("startTime.low", _activityDict)
        print("_startTime_low = " + str(_startTime_low))

        # 通过拼接方式，获取字符串的值，重置当前监听路径，获取拼接后的字符串
        print(_dataConnector.resetByStr("当前房间ID:${user.roomId}")[1])
