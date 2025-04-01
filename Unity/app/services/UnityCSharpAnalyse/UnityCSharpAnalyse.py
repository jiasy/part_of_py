#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from Unity.app.services.UnityCSharpAnalyse.AddStackFuncLog import AddStackFuncLog
from Unity.app.services.UnityCSharpAnalyse.AdjustClassFunc import AdjustClassFunc
from Unity.app.services.UnityCSharpAnalyse.AdjustDelegate import AdjustDelegate
from Unity.app.services.UnityCSharpAnalyse.AdjustIfElse import AdjustIfElse
from Unity.app.services.UnityCSharpAnalyse.AnalyseStructure import AnalyseStructure
from Unity.app.services.UnityCSharpAnalyse.CurlyBraces import CurlyBraces
from Unity.app.services.UnityCSharpAnalyse.DrawClassRelation import DrawClassRelation
from Unity.app.services.UnityCSharpAnalyse.RemoveComment import RemoveComment

from utils import folderUtils
from utils import fileUtils
from utils import pyServiceUtils

import os
import shutil
import yaml
import json
import sys


# 分析 C# 文件，修改其内容，为函数添加输出【最好配合Git，省得在单独备份文件】
class UnityCSharpAnalyse(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        self.funcRegStr = r'^([=\.\[\] ,<>a-zA-Z0-9_\t]*)\s+([a-zA-Z0-9_]+)\s*\(\s*([^\)]*)\s*\)\s*\{'
        self.notFuncNameList = [
            "using", "catch", "lock",
            "if", "switch", "while",
            "for", "foreach"
        ]
        self.funcTypeList = [
            "public", "private", "protected"
        ]
        self.classTypeList = [
            "public", "protected", "internal", "private"  # protected internal
        ]
        self.removeComment: RemoveComment = None
        self.adjustIfElse: AdjustIfElse = None
        self.adjustClassFunc: AdjustClassFunc = None
        self.adjustDelegate: AdjustDelegate = None
        self.curlyBraces: CurlyBraces = None
        self.analyseStructure: AnalyseStructure = None
        self.addStackFuncLog: AddStackFuncLog = None
        self.drawClassRelation: DrawClassRelation = None

    def create(self):
        super(UnityCSharpAnalyse, self).create()
        self.removeComment = self.getSubClassObject("RemoveComment")
        self.adjustIfElse = self.getSubClassObject("AdjustIfElse")
        self.adjustClassFunc = self.getSubClassObject("AdjustClassFunc")
        self.adjustDelegate = self.getSubClassObject("AdjustDelegate")
        self.curlyBraces = self.getSubClassObject("CurlyBraces")
        self.analyseStructure = self.getSubClassObject("AnalyseStructure")
        self.addStackFuncLog = self.getSubClassObject("AddStackFuncLog")
        self.drawClassRelation = self.getSubClassObject("DrawClassRelation")
        return
        # print("正在调整抒写 -- if else")
        # self.adjustIfElse.adjustIfElseFolder(pass :
        #     _baseFolderPath + "C#_removeComment/",
        #     _baseFolderPath + "C#_removeComment_adjust_ifElse/"
        # )

        # print("正在调整抒写 -- delegate")
        # self.adjustDelegate.adjustDelegateFolder(
        #     _baseFolderPath + "C#_removeComment_adjust_classFunc/",
        #     _baseFolderPath + "C#_removeComment_adjust_classFunc_delegate/"
        # )

    def removeCommentAndAdjustLine(self, targetFolder_):
        self.removeComment.removeCSharpCommentInFolder(targetFolder_, targetFolder_)  # 去掉注释
        self.adjustClassFunc.adjustClassFuncVariableLineFolder(targetFolder_, targetFolder_)  # 调整类和变量的括号位置

    # 检查格式调整后，大括号没有闭合的代码
    def checkCurlyBraces(self, targetFolder_: str):
        self.removeCommentAndAdjustLine(targetFolder_)
        _curlyBracesNotCloseFileList = self.curlyBraces.cSharpCurlyBracesFileObject.checkCulyBracesFolder(targetFolder_)
        if len(_curlyBracesNotCloseFileList) > 0:
            print("* 大括号没有闭合的代码 : ")
            for _curlyBracesNotCloseFile in _curlyBracesNotCloseFileList:
                print(_curlyBracesNotCloseFile)

    def analyseClassInfo(self, targetFolder_: str, filterShortNameList_: list = []):
        self.removeCommentAndAdjustLine(targetFolder_)
        return self.analyseStructure.analyseFileInfo(targetFolder_, filterShortNameList_)  # 获取类和方法信息

    # 添加运行日志
    def addRunningStackLog(self, targetFolder_: str, filterClassOrFolderList_: list = []):
        _fileClassFuncDict = self.analyseClassInfo(targetFolder_, filterClassOrFolderList_)
        self.addStackFuncLog.addFuncInOutLogFolder(targetFolder_, targetFolder_, _fileClassFuncDict)  # 添加日志

    # 通过 dot 绘画类之间的关系
    def drawClassRelationInDot(self, targetFolder_: str, filterClassOrFolderList_: list = [], withFolder_: bool = True):
        _fileClassFuncDict = self.analyseClassInfo(targetFolder_, filterClassOrFolderList_)
        if withFolder_:
            self.drawClassRelation.drawClassRelation(_fileClassFuncDict, targetFolder_)
        else:
            self.drawClassRelation.drawClassRelationWithOutFolderStructure(_fileClassFuncDict, targetFolder_, True)

    def syncLogUtils(self, assetPath_: str):
        _logUtilsFolderPath = os.path.join(self.resPath, "LogUtils")
        _targetLogUtilsFolderPath = os.path.join(assetPath_, "LogUtils")
        _logUtilsAsmdefMetaPath = os.path.join(_logUtilsFolderPath, "LogUtils.asmdef.meta")
        _fs = open(_logUtilsAsmdefMetaPath, encoding="UTF-8")  # 打开已经在 Unity 中生成过的 meta
        _yamlData = yaml.load(_fs, Loader=yaml.FullLoader)
        # 没有日志文件就拷贝过去
        if not os.path.exists(_targetLogUtilsFolderPath):
            shutil.copytree(_logUtilsFolderPath, _targetLogUtilsFolderPath)
        return _yamlData["guid"]  # 获得并返回 meta 中的 guid

    # 将 csFolder 中 的 asmdef 引用 LogUtils 的 asmdef 文件
    def linkLogUtilsAsmdef(self, csFolder_: str, logUtilsMetaGuid_: str):
        _asmdefList = folderUtils.getFilePathWithSuffixInFolder(csFolder_, ".asmdef")
        for _i in range(len(_asmdefList)):
            _asmdefPath = _asmdefList[_i]
            print('_asmdefPath = ' + str(_asmdefPath))
            _asmdefDict = fileUtils.dictFromJsonFile(_asmdefPath)
            # logUtils 的 guid
            _logUtilsAsmdefGuid = ("GUID:" + logUtilsMetaGuid_)
            # 在 asmdef 的依赖上查找，如果不在依赖上那么就添加这个
            if "references" in _asmdefDict and _logUtilsAsmdefGuid not in _asmdefDict["references"]:
                # 这个字段是 source compare 比对手动指定 LogUtils.asmdef 得到的
                if "rootNamespace" not in _asmdefDict:
                    _asmdefDict["rootNamespace"] = ""
                # 添加依赖 guid
                _asmdefDict["references"].append(_logUtilsAsmdefGuid)
                _newContent = str(json.dumps(_asmdefDict, indent=4, sort_keys=False, ensure_ascii=False))
                print('_newContent = ' + str(_newContent))
                fileUtils.writeFileWithStr(_asmdefPath, _newContent)

    # 将给定包名的内容移到可编辑区
    def makePackageEdit(self, projectFolderPath_: str, packageNameList_: list):
        # Unity 包缓存路径，获取其包列表
        _packageCacheFolderPath = os.path.join(projectFolderPath_, "Library/PackageCache")
        _folderList = folderUtils.getFolderNameListJustOneDepth(_packageCacheFolderPath)
        # 可编辑的路径，确保其存在
        _editPackagesFolderPath = os.path.join(projectFolderPath_, "Packages")
        folderUtils.makeSureDirIsExists(_editPackagesFolderPath)
        # 拷贝文件夹
        for _idx in range(len(_folderList)):
            _packageNameAndVersion = _folderList[_idx]
            _needMove = False
            for _idxLoop in range(len(packageNameList_)):
                _namespace = packageNameList_[_idxLoop]
                if _namespace in _packageNameAndVersion:
                    _needMove = True
                if _needMove:
                    _fromFolder = os.path.join(projectFolderPath_, _packageNameAndVersion)
                    _package = os.path.basename(_packageNameAndVersion).split("@")[0]  # 去掉版本号
                    _targetFolder = os.path.join(projectFolderPath_, _package)
                    print(_fromFolder + " -> " + _targetFolder)
                    shutil.move(_fromFolder, _targetFolder)

    def destroy(self):
        super(UnityCSharpAnalyse, self).destroy()


if __name__ == '__main__':
    _svr: UnityCSharpAnalyse = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
    sys.exit(1)
    _dataCenterCodeFolderPath = "/Users/nobody/Documents/develop/selfDevelop/Unity/DataCenter/DataCenter/Assets/"
    _unityCSharpAnalyse.drawClassRelationInDot(_dataCenterCodeFolderPath, [
        "Samples/",
        "Editor/HierarchyTools/",
        "Editor/UIToolKit/",
    ])
