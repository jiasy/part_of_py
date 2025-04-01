#!/usr/bin/env python3
from base.supports.Info.Info import Info
from base.supports.Consts.Consts import Consts
from utils import pyUtils
from typing import List
import os
import json


class App(object):
    def __init__(self, appName_: str):
        # 相互关联
        self.main = None
        # app名称
        self.appName: str = appName_[0:-3]
        self.mainPath: str = os.path.realpath(
            os.path.join(os.path.realpath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))
        self.resPath: str = os.path.realpath(
            os.path.join(self.mainPath, self.appName, "res"))
        # 当前的base继承类有那些
        self.runtimeObjectInfoDict: dict = {}
        # 当前的base继承类有多少
        self.baseCount: int = 0
        # 获取 当前App 的 ServiceManager
        self.sm = pyUtils.getObjectByClassPath(self.appName + ("." + self.appName + "ServiceManager") * 2, self)
        self.info = Info(self.sm)
        self.consts = Consts(self.sm)
        self.sm.create()
        self.info.create()
        self.consts.create()
        # 创建 App 状态集合
        self.appState = self.sm.serviceProvider.getAppStateObject(self.appName)
        self.appState.create()

    def __del__(self):
        self.appState.destroy()
        self.sm.destroy()

    # 程序状态重置成唯一一个服务运行
    def getSingleRunningService(self, serviceName_: str):
        self.sm.switchRunningServices([])  # 清理当前
        return self.sm.switchRunningServices([serviceName_])[0]  # 替换上新的

    # 变更 App 状态
    def changeAppState(self, stateName_):
        if stateName_ in self.appState.appStateDict:
            # 获取当前 状态 对应的 服务列表
            _serviceNameList: List[str] = self.appState.appStateDict[stateName_]
            # 按照当前的服务列表，切换服务
            self.sm.switchRunningServices(_serviceNameList)
            # # 显示当前存在的Base子类对象
            # self.sm.showCurrentBaseObejctsInfo()
        else:
            self.info.raiseERR(
                pyUtils.getCurrentRunningFunctionName() + "\n" +
                stateName_ + " : is not in appState\n" +
                str(json.dumps(self.appState.appStateDict, indent=4, sort_keys=False, ensure_ascii=False))
            )

    def getServiceByName(self, serviceName_: str):
        _service = self.sm.getServiceByName(serviceName_)
        if _service is None:
            self.info.raiseERR(
                pyUtils.getCurrentRunningFunctionName() + "\n" +
                serviceName_ + " : is not running\n" +
                str(json.dumps(self.appState.appStateDict, indent=4, sort_keys=False, ensure_ascii=False))
            )
        return _service

    def start(self):
        self.info.raiseERR(
            pyUtils.getCurrentRunningFunctionName() + "App start function must override"
        )

    def doTest(self):
        self.changeAppState("test")


if __name__ == "__main__":
    @pyUtils.timeit
    def createApp(appName_):
        # 确认 app 为单子类
        testApp = App(appName_)
        testApp.start()


    createApp("test")
