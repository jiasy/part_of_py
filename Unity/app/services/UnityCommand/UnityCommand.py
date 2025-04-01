#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import fileUtils
import os
import re
from utils import pyUtils

import plistlib
import sys
import json

'''
from Unity.app.services.UnityCommand import UnityCommand
_svr : UnityCommand = pyServiceUtils.getSvrByName("Unity", "UnityCommand")
'''


class UnityCommand(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(UnityCommand, self).create()

    def destroy(self):
        super(UnityCommand, self).destroy()

    def getUnityAppPath(self, unityVersion_: int):
        _unityPath = None
        if unityVersion_ == 2020:
            _unityPath = "/Applications/Unity/Unity2020.3.23/Unity.app/Contents/MacOS/Unity"
        elif unityVersion_ == 2023:
            _unityPath = "/Applications/Unity/Hub/Editor/2023.1.0a21/Unity.app/Contents/MacOS/Unity"
        if not os.path.exists(_unityPath):
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), "Unity {0} 不存在".format(unityVersion_))
            return
        return _unityPath

    def getPlayerPrefsPath(self, packageName_):
        return os.path.join("/Users/nobody/Library/Preferences", f"unity.{packageName_}.plist")

    def getPlayerPrefs(self, packageName_):
        plist_path = self.getPlayerPrefsPath(packageName_)
        with open(plist_path, 'rb') as fp:
            plist_data = plistlib.load(fp)

        # print(plist_data)

        # # 使用json库中的dumps方法将plist_data转换为JSON字符串
        # json_data = json.dumps(plist_data, indent=4)
        # # 打印输出JSON数据
        # print(json_data)
        return plist_data

    def getPlayerPrefsByKey(self, packageName_, key_):
        return self.getPlayerPrefs(packageName_)[key_]

    def operate_PlayerPrefs_int_set(self, packageName_, key_, tarValue_):
        plist_data = self.getPlayerPrefs(packageName_)
        _curValue = plist_data[key_]
        if isinstance(_curValue, str):  # 字符串可转int
            if _curValue.isdigit():
                plist_data[key_] = str(tarValue_)
            else:
                sys.exit(1)
        elif isinstance(_curValue, int):  # 本身就是 int
            plist_data[key_] = tarValue_
        else:
            sys.exit(1)
        plist_path = self.getPlayerPrefsPath(packageName_)
        with open(plist_path, 'wb') as fp:
            plistlib.dump(plist_data, fp)

    # 运行时，Unity 有缓存，对plist的修改，需要重启编辑器才生效
    def operate_PlayerPrefs_int_add(self, packageName_, key_):
        plist_data = self.getPlayerPrefs(packageName_)
        _value = plist_data[key_]
        if isinstance(_value, str):  # 字符串可转int
            if _value.isdigit():
                _value = int(_value) + 1
                plist_data[key_] = str(_value)
            else:
                sys.exit(1)
        elif isinstance(_value, int):  # 本身就是 int
            _value = _value + 1
            plist_data[key_] = _value
        else:
            sys.exit(1)
        plist_path = self.getPlayerPrefsPath(packageName_)
        with open(plist_path, 'wb') as fp:
            plistlib.dump(plist_data, fp)
        return _value

    # 获取日志内的第一次报错信息
    def getLogFirstErrorStr(self, unityLogPath_: str):
        pattern = r"Exception:(.*?)(?=\(Filename:)"
        match = re.search(pattern, fileUtils.readFromFile(unityLogPath_), re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return None


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils

    # 自增
    # _svr.operate_PlayerPrefs_int_add(Company_BB_Utils.getSLGDevelopPackName(), "x_K_Accunt_Info_Pid_Uid")
    _int = _svr.getPlayerPrefsByKey(Company_BB_Utils.getSLGDevelopPackName(), "x_K_Accunt_Info_Pid_Uid")
    # _int = _svr.getPlayerPrefsByKey(Company_BB_Utils.getSLGDevelopPackName(), "ResetTimes")
    print('_int = ' + str(_int))
