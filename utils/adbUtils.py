#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from utils import sysUtils
from utils import cmdUtils
from utils import listUtils
from utils import folderUtils
from utils import fileUtils
from utils import strUtils
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import functools
import os

_thisFilePath = os.path.dirname(os.path.realpath(__file__))
print("脚本路径 : " + _thisFilePath)
_pwd = sysUtils.folderPathFixEnd(os.getcwd())
print("执行路径 : " + _pwd)

colorList = ["blue", "cyan", "green", "indigo", "red", "darkred", "yellow", "brown", "orchid", "tomato", "orangered",
             "chocolate"]


class MemKeyInfo:
    # 运行中可能忽然增加一个键，这个时候要将前面的帧都填充成 0
    def __init__(self, key_: str, count_: int = 0):
        self.key = key_
        self.mbList = []
        self.colorIdx = -1
        self.maxMB = -1
        for _i in range(0, count_):
            self.mbList.append(0)

    def add(self, num_: int):
        _MB = round(num_ / 1024)
        self.mbList.append(_MB)

    def toPic(self, folderPath_: str, colorIdx_: int):  # 绘图
        self.maxMB = listUtils.maxInList(self.mbList)
        # 最大都不超过10MB就不用生成图了。。。
        if self.maxMB < 10:
            return False
        self.colorIdx = colorIdx_
        _x = np.arange(len(self.mbList))  # x 轴
        plt.figure(colorIdx_ + 2)  # 指向不同的图，1还是整图的
        plt.bar(_x, self.mbList, width=1, fc=colorList[self.colorIdx])
        # 图片宽高（单位是100像素）
        plt.gcf().set_size_inches(20, 5)
        # x轴每多少放置一个标
        x_major_locator = MultipleLocator(50)
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        # 标题
        plt.title(self.key)
        # 轴上起止坐标
        plt.ylim(0, self.maxMB * 1.1)  # y 轴放大1.1，上方有点儿空间
        plt.xlim(0, len(self.mbList))  # x轴按照个数做起止坐标
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(folderPath_, self.key.replace(".", "_").replace(" ", "_") + ".png"))
        return True

    def printSelf(self):
        listUtils.printList(self.mbList, self.key + " : ")


class MemInfoMgr:
    def __init__(self, logFolder_: str):
        self.keyToMemDict = {}  # 每一个键的逐帧内存情况
        _logList = folderUtils.getFilterFilesInPath(logFolder_, [".txt"])
        _logList = sorted(_logList)
        for _i in range(len(_logList)):
            self.analyseLog(_logList[_i], _i)  # 缓存数据

    def toPic(self, picFolder_: str):
        _colorIdx = 0
        _mbInfoList = []
        for _key in self.keyToMemDict:
            if _key == "TOTAL":  # 不记录 TOTAL 的数据
                continue
            if self.keyToMemDict[_key].toPic(picFolder_, _colorIdx):  # 只有其最大峰值超过10MB才会记录
                _mbInfoList.append(self.keyToMemDict[_key])  # 记录数组
                _colorIdx += 1

        # 获取内存
        _totalMbList = self.keyToMemDict["TOTAL"].mbList  # TOTAL的内存数据
        _maxMB = listUtils.maxInList(_totalMbList)  # 获取 TOTAL的最大值
        plt.figure(1)  # 1是整图的
        _x = np.arange(len(_totalMbList))  # x 轴
        # 底
        _bottomList = []
        for _i in range(len(_totalMbList)):
            _bottomList.append(0)
        # SAMPLE - 列表排序，使用函数（倒叙）
        _mbInfoList = sorted(_mbInfoList, key=functools.cmp_to_key(self.sortFunc), reverse=True)
        # 更新底，画图
        for _i in range(len(_mbInfoList)):
            _mbInfo = _mbInfoList[_i]
            plt.bar(
                _x, _mbInfo.mbList, bottom=_bottomList, width=1, fc=colorList[_mbInfo.colorIdx],
                label=_mbInfo.key
            )
            _bottomList = self.getBottom(_bottomList, _mbInfo.mbList)  # 叠加底

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

    # 根据最大内存使用排个顺序
    def sortFunc(self, info1_: MemKeyInfo, info2_: MemKeyInfo):
        # 小的在前面
        if info1_.maxMB > info2_.maxMB:
            return -1
        elif info1_.maxMB == info2_.maxMB:
            return 0
        else:
            return 1

    def getBottom(self, bottom_: list, memList_: list):
        _newBottom = []
        for _i in range(len(bottom_)):
            _newBottom.append(bottom_[_i] + memList_[_i])
        return _newBottom

    def printSelf(self):
        for _key in self.keyToMemDict:
            self.keyToMemDict[_key].printSelf()

    def analyseLog(self, logPath_: str, idx_: int):
        _lines = fileUtils.linesFromFileWithOutEncode(logPath_)
        '''
         App Summary
                       Pss(KB)
                        ------
           Java Heap:     7776
         Native Heap:   301684
                Code:   109468
               Stack:       80
            Graphics:   377984
       Private Other:  1607604
              System:   247566

               TOTAL:  2652162       TOTAL SWAP PSS:   228310
        '''
        # 删


def getThridPackageList():
    '''
    列出第三方安装包，显示如下格式（展示一小部分）
    package:com.tencent.mobileqq
    package:com.xxx.XM01
    package:com.xxx.XM02
    package:com.baidu.BaiduMap
    '''
    # 删


def getPackageName():
    _packageStrList = getThridPackageList()  # 列出第三方包名，包括自己装的
    _characteristic = "pj.dev"
    for _i in range(len(_packageStrList)):
        _packageName = _packageStrList[_i]
        if _characteristic in _packageName:
            return _packageName
    print("手机没有指定特征的包")
    sys.exit(1)


def getPackageNameBy(characteristic_):
    _packageStrList = getThridPackageList()  # 列出第三方包名，包括自己装的
    _version = 0
    _targetPackageName = None
    for _i in range(len(_packageStrList)):
        _packageName = _packageStrList[_i]
        if characteristic_ in _packageName:
            print('_packageName = ' + str(_packageName))
            _tempVersion = int(_packageName.split(characteristic_)[1])  # 版本
            if _tempVersion > _version:  # 取最高版本包名
                _targetPackageName = _packageName
                _version = _tempVersion
    # 获取最高版本的包名
    if _targetPackageName is not None:
        print('_targetPackageName = ' + str(_targetPackageName))
        return _targetPackageName
    else:
        print("手机没有指定特征的包")
        sys.exit(1)


# 获取 指定包名 运行时 的 pid
def getRuntimePid(packageName_):
    # 获取包的运行信息，确保其处于运行中
    _processStrList = cmdUtils.doStrAsCmdAndGetPipeline("adb shell ps | grep " + packageName_, _pwd)
    if not _processStrList:
        print(packageName_ + " 不在运行中")
        return None
    '''
    过滤出来的内容有两行，第一行为推送的包名
    u0_a484      29763   662 5167588  72208 0                   0 S com.xxx.XM02:push_xx
    u0_a484      30766   662 11566688 509036 0                  0 S com.xxx.XM02
    '''
    _pid = None
    # 获取 pid
    for _i in range(len(_processStrList)):
        _processInfoStr = _processStrList[_i]
        _processInfoStr = ' '.join(_processInfoStr.split())
        if not (":push" in _processInfoStr):
            _pid = _processInfoStr.split(' ')[1]
    return _pid


# 运行指定 app
def runPackage(packageName_):
    _mainActivity = getMainActivity(packageName_)
    if _mainActivity is None:
        print(packageName_ + " 没有对应的 mainActivity")
        sys.exit(1)

    # 启动 app 至给定 Activity
    cmdUtils.doStrAsCmd(
        "adb shell am start -n {0}/{1}".format(packageName_, _mainActivity),
        _pwd,
        False
    )


# 输出当前前端运行的 app 的包名
def getCurrentRunningAppPackageName():
    # 获取 CPU 平台厂商
    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell dumpsys window", _pwd
    )
    #  mCurrentFocus=Window{3167b05 u0 com.xxx.yyy.zzz/com.xxx.main.MainActivity}
    for _i in range(len(_cmdResult)):
        _line = _cmdResult[_i]
        if "mCurrentFocus" in _line:
            _packageName = _line.split(" ")[-1].split("/")[0]
            return _packageName
    return None


# 获取App日志。
def getRuntimeLogCmd():
    # 启动
    _pid = runAppThenGetPid()
    # 收集日志的命令
    _cmdRuntime = "adb shell logcat | grep --color=auto " + _pid
    print('_cmdRuntime = ' + str(_cmdRuntime))
    return _cmdRuntime


# 获取App内存信息
def getMemInfoCmd():
    # 启动
    _pid = runAppThenGetPid()
    # 内存信息e
    _cmdMemInfo = getMemInfoCmdByPid(_pid)
    print('_cmdMemInfo = ' + str(_cmdMemInfo))
    return _cmdMemInfo


# 获取 Mem Info cmd 命令
def getMemInfoCmdByPid(pid_: str):
    return "adb shell dumpsys meminfo " + pid_


# 获取 GPU Info cmd 命令
def getGPUInfoCmdByPid(pid_: str):
    return "adb shell dumpsys gfxinfo " + pid_


# 获取 CPU Info cmd 命令
def getCPUInfoCmdByPid(packagePrefix_: str):
    # TODO 过滤出给定的前缀，所占的百分比
    return "adb shell top -m 10 > "


# 获取 当前链接 的 设备 ID
def getDeviceID():
    return getDeviceList()[0]


# 获取 设备列表
def getDeviceList():
    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb devices -l",
        _pwd
    )
    _deviceList = []
    for _i in range(1, len(_cmdResult) - 1):
        _resultLine = strUtils.spacesReplaceToSpace(_cmdResult[_i])
        _deviceList.append(_resultLine.split(" ")[0])
    return _deviceList


# 自动获取包名对应的pid
def runAppThenGetPid():
    cmdUtils.doStrAsCmdAndGetPipeline("adb wait-for-device", _pwd)
    # 自动获取包名
    _packageName = getPackageName()
    # 获取运行中的 package 对应的 pid
    _pid = getRuntimePid(_packageName)
    # 取到了，打印出要执行的 shell
    if _pid is None:
        print("没有处于运行状态，尝试启动 app")
        runPackage(_packageName)  # 运行 app
        _pid = getRuntimePid(_packageName)  # 再次获取 运行 pid
    else:
        print("处于运行状态中")
    return _pid


# get_Unity_Resources_UnloadUnusedAssets_Log("com.xxx.yyy")
def get_Unity_Resources_UnloadUnusedAssets_Log(packageName_: str):
    _pid = getRuntimePid(packageName_)
    _cmd = "adb shell logcat | grep --color=auto -E \" Unloading |System memory in use | Total: \""
    print(_cmd)


# get_Unity_Profiler_Connect("com.xxx.yyy",55001)
def get_Unity_Profiler_Connect(packageName_: str, port_: int):
    return "adb forward tcp:" + str(port_) + " localabstract:" + packageName_


# 打印 手机信息
def getDeviceInfo():
    # 获取 CPU 平台厂商
    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell cat proc/cpuinfo | grep Hardware", _pwd
    )
    print("CPU 平台 : " + _cmdResult[0])
    # 看是几核心的
    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell ls -l /sys/devices/system/cpu/ | grep -n 'cpu[0-9]*$'", _pwd
    )
    _coreCount_1 = len(_cmdResult)
    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell cat proc/cpuinfo | grep processor", _pwd
    )
    _coreCount_2 = len(_cmdResult)
    if _coreCount_1 == _coreCount_2:
        print("CPU 核心数 : " + str(_coreCount_2))
    else:
        print("CPU 核心数 获取不一致 : " + str(_coreCount_1) + "  - " + str(_coreCount_2))
        sys.exit(1)

    # 获取 最高、最低 主频
    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell cat sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq", _pwd
    )
    print("主频最高 : {}GHZ".format(str(int(int(_cmdResult[0]) / 1000))))
    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell cat sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq", _pwd
    )
    print("主频最底 : {}GHZ".format(str(int(int(_cmdResult[0]) / 1000))))
    # 获取 电池 温度
    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell dumpsys battery | grep temperature", _pwd
    )
    print("电池温度 : {}度".format(str(float(int(_cmdResult[0].split("temperature: ")[1]) / 100))))

    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell ip addr show wlan0 | grep inet'\ '", _pwd
    )
    print("IP地址 : {}".format(_cmdResult[0].split("inet")[1].split("brd")[0].replace(" ", "").split("/")[0]))


# 文件发送到SD卡
def pushToSD(localPath_: str, sdFolderPath_: str):
    # 删


# 文件拉取到本地
def pullFromSD(sdPath_: str, localFolderPath_: str):
    # 删


# 截图
def doScreencap(screenCapName_="screenCap"):
    _screenPath = os.path.join("", "sdcard/DCIM", screenCapName_ + ".png")
    cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell screencap -p {0}".format(_screenPath),
        _pwd
    )
    return _screenPath


# 得到包名对应的主Activity
def getMainActivity(packageName_: str):
    _cmdResult = cmdUtils.doStrAsCmdAndGetPipeline(
        "adb shell monkey -c android.intent.category.LAUNCHER -v -v -v  0",
        _pwd
    )
    for _i in range(len(_cmdResult)):
        _resultLine = _cmdResult[_i]
        _activityAndPackageResult = re.search(r'.* Using main activity (.+) \(.*from package (.+)\)', _resultLine)

        if _activityAndPackageResult:
            if _activityAndPackageResult.group(2) == packageName_:
                return _activityAndPackageResult.group(1)
    return None


# 链接一个手机，生成针对手机的apks并安装
def aabInstall(bundleToolPath_: str, aabPath_: str, apksPath_: str):
    _cmd = "java -jar {0} build-apks --bundle={1} --output={2} --local-testing --connected-device".format(
        bundleToolPath_,
        aabPath_,
        apksPath_
    )
    cmdUtils.doStrAsCmd(_cmd, os.getcwd())
    _cmd = "java -jar {0} install-apks --apks={1}".format(
        bundleToolPath_,
        apksPath_
    )
    cmdUtils.doStrAsCmd(_cmd, os.getcwd())


# 在设备上点开一个输入框，然后执行该脚本
def fillStrOnDevice(str_: str):
    # 删


# 获取文件夹内的文件列表
def do_LS_onPath(deviceId_: str, path_: str):
    # 删
    return _fileList


# 获取存储的根节点
def getStorageRoot():
    return "/storage/emulated/0/"


if __name__ == '__main__':
    # get_Unity_Resources_UnloadUnusedAssets_Log("com.xxx.pj.dev")
    # _pid = getRuntimePid("com.xxx.pj.rel")
    # print("adb shell logcat | grep --color=auto " + str(_pid))

    # # 获取 输出实时日志 命令
    # _cmdRuntime = getRuntimeLogCmd()
    # # 获取 内存信息
    # _cmdRuntime = getMemInfoCmd()

    # # 截屏，并保存到本地
    # _screenCapFilePath = doScreencap()
    # print('_screenCapFilePath = ' + str(_screenCapFilePath))
    # pullFromSD(_screenCapFilePath, "/Users/nobody/Downloads/screenCapOnAndroid/")

    # 获取 package name
    # getPackageNameBy("partOfName")

    # # 获取 设备 信息
    # getDeviceInfo()
    #
    # # 获取当前运行的 App 包名
    # _packageName = getCurrentRunningAppPackageName()
    # print('当前运行 APP : ' + str(_packageName))

    # # 获取 指定 包名的 MainActivity
    # _mainActivityName = getMainActivity(Company_BB_Utils.getJPReleasePackName())
    # print('_mainActivityName = ' + str(_mainActivityName))

    # # 在设备的输入框填充文本
    # # fillStrOnDevice('UIHelper.GetPageByMetaId(EUIPage.ServiceListPage).cs_page.transform:Find("obj_spine").gameObject:SetActive(false)')
    fillStrOnDevice('NotifyMgr:ShowTip(_VERSION)\n')
    fillStrOnDevice('NotifyMgr:ShowTip(tostring(jit))\n')

    # # 当前运行的 app 文件列表
    # _deviceID = getDeviceID()
    # # 截屏的路径
    # _androidFolderPath = os.path.join(getStorageRoot(), "koreader/screenshots/")
    # # 打印截屏路径中的内容
    # listUtils.printList(do_LS_onPath(_deviceID, _androidFolderPath), "")
