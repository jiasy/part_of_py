#!/usr/bin/env python3
# 引用方式 from Excel.app.services.Document import Document
from utils import pyServiceUtils
from utils import excelControlUtils
from base.supports.Service.BaseService import BaseService
from utils import folderUtils
from utils import fileUtils
import sys

excelFolderPath = "/Users/nobody/Documents/develop/Excel/"

excelDict = {
    # mac
    "无法确认开发者的库赋予权限 - 无法打开，提示扔进废纸篓": ["Android", "环境", "AR181"],
    # Unity
    "资源引用基础概念": ["PJ代码阅读", "AssetManager", "AU120"],
    "动画": ["渲染", "animation", "A1"],
    "粒子效果": ["渲染", "particle", "A1"],
    "C#的GC": ["GM+性能日志", "C#", "DH24"],
    "XLua引用C#对象与清理": ["PJ代码阅读", "XLua", "BU821"],
    "修改资源参数": ["C#_Unity", "Tools", "B2"],
    "运行时获取平台信息": ["C#_Unity", "Tools", "AY2"],
    "ECS": ["C#_Unity", "ECS", "A1"],
    "JobSystem": ["C#_Unity", "JobSystem", "A1"],
    "Package可写": ["GM+性能日志", "插件", "DM141"],
    "Lua模拟环境": ["SelfFrame", "LuaDev", "CK34"],
    "Editor-Execute-Lua": ["SelfFrame", "LuaDev", "AQ132"],
    "QualitySettings": ["渲染", "基础", "BU276"],
    # 渲染
    "颜色空间": ["渲染", "基础", "BP40"],
    "Material": ["渲染", "Shader", "BO30"],
    "ShaderLab基础": ["渲染", "Shader", "W95"],
    "SRP": ["渲染", "SRP", "A1"],
    "动静和批": ["渲染", "Batch+Mesh", "BF47"],
    "GPUInstance": ["渲染", "Batch+Mesh", "AQ129"],
    "SRPBatcher基础": ["渲染", "Batch+Mesh", "AX190"],
    "SRPBatcher监控": ["渲染", "Batch+Mesh", "GG242"],
    "Android下粒子效果Mesh要开读写": ["渲染", "Batch+Mesh", "GG242"],
    # lua
    "next判断列表是否为空": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "RM204"],
    "Data数据绑定": ["PJ代码阅读", "initData", "KK60"],
    "LuaState清理": ["PJ代码阅读", "生命周期，登陆，断线", "AR051"],
    "luaEvent": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "TD173"],
    "require流程": ["PJ代码阅读", "Xlua初始化", "BG719"],
    "require流程，lua变更直接生效": ["PJ代码阅读", "lua Require 过程", "AB126"],
    "Lua内存泄漏排查": ["PJ代码阅读", "XLua", "X1014"],
    # common
    "时间段的判断": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "MO240"],
    "按秒倒计时": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "NM175"],
    "服务器请求流程": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "IY305"],
    "通用对象池": ["PJ代码阅读", "生命周期，登陆，断线", "GS298"],
    "AssetReference与业务关联后的清理": ["PJ代码阅读", "本地化", "FL78"],
    "AssetsMgr表层": ["PJ代码阅读", "UI_界面加载", "FE368"],
    "AssetReference清理": ["PJ代码阅读", "生命周期，登陆，断线", "AS438"],
    "AssetReference创建": ["PJ代码阅读", "生命周期，登陆，断线", "GC454"],
    "资源引用管理代码": ["PJ代码阅读", "AssetManager", "EP33"],
    # bb-UI
    "手势": ["PJ代码阅读", "UI控件", "I32"],
    "列表元素为Toggle按钮": ["PJ代码阅读", "UI控件", "E260"],
    "UI_LuaPart创建": ["PJ代码阅读", "UI_界面加载", "EQ437"],
    "UI_OpenPage流程": ["PJ代码阅读", "UI_界面加载", "BQ151"],
    "UI_翻译": ["PJ代码阅读", "UI_界面加载", "CF570"],
    "UILuaPage_生命周期方法": ["PJ代码阅读", "UI_界面加载", "FE657"],
    "LuaPart_编辑器": ["PJ代码阅读", "UI_界面加载", "DU486"],
    "UI_图片翻译": ["PJ代码阅读", "本地化", "AF77"],
    # bb-logic
    "奖励列表封装": ["PJ代码阅读", "UI控件", "IU68"],
    "启动时的请求队列": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "AV129"],
    "判断-功能-是否开启": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "FR235"],
    "判断-活动-是否开启": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "LP239"],
    "道具个数获取以及判断": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "FD96"],
    "活动配置表关系": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "UY3"],
    "红点配置": ["PJ代码阅读", "SevenDay+网络+周期+功能开启器和GOTO", "YF253"],
    "资源对象池": ["PJ代码阅读", "AssetManager", "AG29"],
    # build - android
    "aab解压apks及安装": ["Android", "Apk", "Apk&Aab"],
    "android环境配置及adb使用": ["Android", "环境", "BM46"],
    "android手机链接UnityProfiler": ["Android", "环境", "EW157"],
    "android手机内存分析": ["GM+性能日志", "内存", "AS21"],
    "Unity反射Java申请Android权限": ["Android", "runtime", "BW32"],
}


class Document(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        self.excelPathDict = folderUtils.getFilePathKeyValue(excelFolderPath, [".xlsx"])

    def create(self):
        super(Document, self).create()

    def destroy(self):
        super(Document, self).destroy()

    # 获得Excel的实际路径
    def getExcelPath(self, justName_: str):
        for _path in self.excelPathDict:
            if fileUtils.justName(_path) == justName_:
                return self.excelPathDict[_path]
        return None

    # 打开并停止到指定功能位置
    def goto(self, func_: str):
        if func_ not in excelDict:
            utils.printUtils.pError("ERROR : 没有此记录 : " + func_)
            sys.exit(1)
        else:
            _funcInfoList = excelDict[func_]
            excelFileName = _funcInfoList[0]
            _excelPath = self.getExcelPath(excelFileName)
            if not _excelPath:
                utils.printUtils.pError("ERROR : 没有此文件 : " + excelFileName)
                sys.exit(1)
            sheetName = _funcInfoList[1]
            cellLocation = _funcInfoList[2]
            excelControlUtils.openCell(
                _excelPath,
                sheetName,
                cellLocation
            )


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    _svr.goto("Unity反射Java申请Android权限")
