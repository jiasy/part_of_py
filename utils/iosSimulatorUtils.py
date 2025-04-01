from utils import cmdUtils
from utils import listUtils
import utils.printUtils
import sys


def getDeviceInfoDict():
    '''
    执行命令的输出
== Device Types ==
...
== Runtimes ==
iOS 16.0 (16.0 - 20A360) - com.apple.CoreSimulator.SimRuntime.iOS-16-0
== Devices ==
-- iOS 16.0 --
    IOS_Simulator (442B99E7-95EB-483A-A9F0-DBA5EA77D0F2) (Shutdown)
== Device Pairs ==
    '''
    _pipline = cmdUtils.doCmdAndGetPiplineList(
        "xcrun",
        "simctl",
        "list"
    )
    _deviceInfo = _pipline.split("== Devices ==")[1].split("== Device Pairs ==")[0]  # 在结构中切出数据
    _deviceInfoLines = _deviceInfo.split("\n")
    if len(_deviceInfoLines) < 3:
        utils.printUtils.pError("ERROR - 没有模拟器对象")
        sys.exit(1)
    listUtils.list_pop(_deviceInfoLines)  # 移除首尾行，剩下的都是有用数据
    listUtils.list_shift(_deviceInfoLines)
    _currentType = None
    _deviceInfoDict = {}
    for _i in range(len(_deviceInfoLines)):
        _line = _deviceInfoLines[_i]
        if _line.startswith("-- "):  # 类别
            _currentType = _line.split("--")[1].replace(" ", "")  # 获取类型，去除空格
        else:  # 模拟器
            _strList = _line.split(" (")
            _name = _strList[0].replace(" ", "")
            _id = _strList[1].split(")")[0]
            _state = _strList[2].split(")")[0]
            _deviceInfoDict[_name] = {}
            _deviceInfoDict[_name]["name"] = _name  # 设备名称
            _deviceInfoDict[_name]["id"] = _id  # 设备ID
            _deviceInfoDict[_name]["state"] = _state  # 设备状态
            _deviceInfoDict[_name]["type"] = _currentType  # 操作系统版本
    return _deviceInfoDict


# 设备是否启动
def isDeviceBooted(deviceNameOrID_: str):
    if deviceNameOrID_ in _deviceInfoDict.keys():  # 设备别名来关联
        if _deviceInfoDict[deviceNameOrID_]["state"] == "Booted":
            return True
    else:  # 设备 ID 来关联
        for _key in _deviceInfoDict:
            if _deviceInfoDict[_key]["id"] == deviceNameOrID_:
                if _deviceInfoDict[_key]["state"] == "Booted":
                    return True
    return False


# 启动指定设备
def bootDevice(deviceNameOrID_: str):
    if not isDeviceBooted(deviceNameOrID_):
        cmdUtils.doCmdAndGetPiplineList("xcrun", "simctl",
                                        "boot",
                                        deviceNameOrID_
                                        )
        return True
    else:
        return False


# 打开指定应用
def bootApp(deviceNameOrID_: str, appBundleIdentifier_: str):
    if bootDevice(deviceNameOrID_):
        privacyAll(_appBundleIdentifier)  # 添加权限
        cmdUtils.doCmdAndGetPiplineList("xcrun", "simctl",
                                        "launch",
                                        deviceNameOrID_, appBundleIdentifier_
                                        )
        return cmdUtils.doCmdAndGetPiplineList("xcrun", "simctl",
                                               "get_app_container",
                                               deviceNameOrID_, appBundleIdentifier_
                                               )
    else:
        return None


# 赋予所有权限
def privacyAll(appBundleIdentifier_: str):
    cmdUtils.doCmdAndGetPiplineList("xcrun", "simctl",
                                    "privacy", "booted", "revoke", "all",
                                    appBundleIdentifier_)


if __name__ == '__main__':
    _deviceInfoDict = getDeviceInfoDict()  # 获取 模拟器信息
    _targetDeviceName = "IOS_Simulator"  # 目标设备
    _appBundleIdentifier = "com.2x2.Skywire"  # 目标应用

    # 启动应用
    _appContainerPath = bootApp(_targetDeviceName, _appBundleIdentifier)
    if _appContainerPath == None:
        utils.printUtils.pError("ERROR : App Boot Fail")
        sys.exit(1)

    print(_appContainerPath)
