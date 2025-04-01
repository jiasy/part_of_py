import os
import Main
from utils import pyUtils


# 可能是服务，也可能是子服务
def getProgramInfo(filePath_):
    _folderPath = os.path.dirname(os.path.realpath(filePath_))
    _folderSplit = os.path.split(_folderPath)
    _servicesOrSvrSplit = os.path.split(_folderSplit[0])
    _serviceOrSvr = _servicesOrSvrSplit[1]
    _svrName = None
    _subSvrName = None
    _serviceSplit = None
    if _serviceOrSvr == "services":
        _svrName = _folderSplit[1]
        _subSvrName = None
        _serviceSplit = _servicesOrSvrSplit
    else:
        _serviceSplit = os.path.split(_servicesOrSvrSplit[0])
        _svrName = _servicesOrSvrSplit[1]
        _subSvrName = _folderSplit[1]

    _appSplit = os.path.split(_serviceSplit[0])
    _appNameSplit = os.path.split(_appSplit[0])
    _appName = _appNameSplit[1]

    return _appName, _svrName, _subSvrName


# 通过 appName_ 指定启动一个App
def getApp(appName_):
    _main = Main.Main()
    if appName_ in _main.appDict:
        return _main.appDict[appName_]
    _app = _main.getAppByName(appName_)
    _app.start()
    return _app


# 根据名称获取 Service
def getSvrByName(appName_, svrName_):
    _app = getApp(appName_)
    _svr = _app.sm.getServiceByName(svrName_)
    if _svr is None:
        _svr = _app.getSingleRunningService(svrName_)
    return _svr


# 根据名称获取 SubService
def getSubSvrByName(appName_, svrName_, subSerName_):
    _svr = getSvrByName(appName_, svrName_)
    _subSvr = _svr.getSubClassObject(subSerName_)
    return _subSvr


# 从当前位的目录置获取所在的Service
def getSvr(filePath_):
    _appName, _svrName, _subSvrName = getProgramInfo(filePath_)
    if _subSvrName is not None:
        raise pyUtils.AppError("当前所在文件是 子服务 : " + _svrName + " -> " + _subSvrName)
    return getSvrByName(_appName, _svrName)


def printSvrCode(filePath_):
    # service 代码生成
    _appName, _svrName, _subSvrName = getProgramInfo(filePath_)
    if _subSvrName is not None:
        raise pyUtils.AppError("当前所在文件是 子服务 : " + _svrName + " -> " + _subSvrName)
    _codeStr = "\n"
    _codeStr += "from {appName}.app.services.{svrName} import {svrName}\n".format(appName=_appName, svrName=_svrName)
    _codeStr += "_svr : {svrName} = pyServiceUtils.getSvrByName(\"{appName}\", \"{svrName}\")\n".format(appName=_appName, svrName=_svrName)
    _codeStr += "\n"
    print(_codeStr)


# 从当前位的目录置获取所在的SubService
def getSubSvr(filePath_: str):
    """

    :rtype: object
    """
    _appName, _svrName, _subSvrName = getProgramInfo(filePath_)
    if _subSvrName is None:
        raise pyUtils.AppError("当前所在文件是 主服务 : " + _svrName)
    return getSubSvrByName(_appName, _svrName, _subSvrName)


def printSubSvrCode(filePath_):
    # service 代码生成
    _appName, _svrName, _subSvrName = getProgramInfo(filePath_)
    if _subSvrName is None:
        raise pyUtils.AppError("当前所在文件是 主服务 : " + _svrName)
    _codeStr = "\n"
    _codeStr += "from {appName}.app.services.{svrName} import {svrName}\n".format(appName=_appName, svrName=_svrName)
    _codeStr += "from {appName}.app.services.{svrName}.{subSvrName} import {subSvrName}\n".format(appName=_appName, svrName=_svrName, subSvrName=_subSvrName)
    _codeStr += "_svr : {svrName} = pyServiceUtils.getSvrByName(\"{appName}\", \"{svrName}\")\n".format(appName=_appName, svrName=_svrName)
    _codeStr += "_subSvr : {subSvrName} = pyServiceUtils.getSubSvrByName(\"{appName}\", \"{svrName}\",\"{subSvrName}\")\n".format(appName=_appName, svrName=_svrName, subSvrName=_subSvrName)
    _codeStr += "\n"
    print(_codeStr)
