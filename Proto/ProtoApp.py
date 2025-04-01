#!/usr/bin/env python3
import sys

from Proto.app.services.ExcelDataToProtoBin.ExcelDataToProtoBin import ExcelDataToProtoBin
from Proto.app.services.ExcelToProtoStruct.ExcelToProtoStruct import ExcelToProtoStruct
from Proto.app.services.ProtoToClass.ProtoToCsClass.ProtoToCsClass import ProtoToCsClass
from Proto.app.services.ProtoToClass.ProtoToPyClass.ProtoToPyClass import ProtoToPyClass
from base.supports.App.App import App
from utils import folderUtils
from utils import fileUtils
from utils import strUtils
from utils import pyServiceUtils
import os


class ProtoApp(App):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    def start(self):
        return

    def testStart(self):
        self.start()

    def getFileDict(self, targetFolder_: str, filterList_: list[str]):
        _fileDict = {}
        _filePathList = folderUtils.getFileListInFolder(targetFolder_, filterList_)
        for _i in range(len(_filePathList)):
            _filePath = _filePathList[_i]  # excel 文件路径
            _justFileName = fileUtils.justName(_filePath)  # excel 的纯名
            if not strUtils.isValidCodeName(_justFileName):
                continue
            _fileDict[_justFileName] = _filePath
        return _fileDict

    def getExcelFileDict(self, targetFolder_: str):
        return self.getFileDict(targetFolder_, [".xlsm"])

    def getProtoFileDict(self, targetFolder_: str):
        return self.getFileDict(targetFolder_, [".proto"])

    def getPyFileDict(self, targetFolder_: str):
        return self.getFileDict(targetFolder_, [".py"])

    def getBinFileDict(self, targetFolder_: str):
        return self.getFileDict(targetFolder_, [".bin"])

    def getFile(self, targetFolder_: str, targetJustName_: str, filterList_: list[str]):
        fileDict = self.getFileDict(targetFolder_, filterList_)
        if targetJustName_ not in fileDict:
            print(f"ERROR : {targetFolder_} - {targetJustName_} 不存在 {filterList_}")
            sys.exit(1)
        return fileDict[targetJustName_]

    def getBinFile(self, targetFolder_: str, targetJustName_: str):
        return self.getFile(targetFolder_, targetJustName_, [".bin"])

    def getExcelFile(self, targetFolder_: str, targetJustName_: str):
        return self.getFile(targetFolder_, targetJustName_, [".xlsm"])

    def getProtoFile(self, targetFolder_: str, targetJustName_: str):
        return self.getFile(targetFolder_, targetJustName_, [".proto"])

    def getPyFile(self, targetFolder_: str, targetJustName_: str):
        return self.getFile(targetFolder_, targetJustName_, [".py"])

    def stateToExcelToBin(self, nameSpace_: str):
        self.changeAppState("excelToBin")
        _excelToProtoStruct: ExcelToProtoStruct = self.getServiceByName("ExcelToProtoStruct")  # proto 结构定义文件生成
        _excelDataToProtoBin: ExcelDataToProtoBin = self.getServiceByName("ExcelDataToProtoBin")  # Excel 内容转换成Bin
        _protoToClass: ProtoToClass = self.getServiceByName("ProtoToClass")  # 代码 生成
        _protoToClass.protoToPyClass = _protoToClass.getSubClassObject("ProtoToPyClass")  # 生成 py
        _protoToPyClass: ProtoToPyClass = _protoToClass.protoToPyClass
        _protoToClass.protoToCsClass = _protoToClass.getSubClassObject("ProtoToCsClass")  # 生成 cs
        _protoToCsClass: ProtoToCsClass = _protoToClass.protoToCsClass

        _protoFolder = os.path.join(_excelToProtoStruct.resPath, nameSpace_)  # proto 承载
        folderUtils.makeSureDirIsExists(_protoFolder)
        _pyCodeFolder = os.path.join(_protoToPyClass.subResPath, nameSpace_)  # py 承载
        folderUtils.makeSureDirIsExists(_pyCodeFolder)
        _binFolder = os.path.join(_excelDataToProtoBin.resPath, nameSpace_)  # bin 承载
        folderUtils.makeSureDirIsExists(_binFolder)
        _csCodeFolder = os.path.join(_protoToCsClass.subResPath, nameSpace_)  # cs 承载
        folderUtils.makeSureDirIsExists(_csCodeFolder)
        folderUtils.makeSureDirIsExists(os.path.join(_csCodeFolder, "AutoCreateClass"))  # 生成代码向下放一级

        return _excelToProtoStruct, _excelDataToProtoBin, _protoToPyClass, _protoToCsClass, _protoFolder, _binFolder, _pyCodeFolder, _csCodeFolder

    def excelFolderToBin(self, dataCacheFolder_: str, excelFolder_: str, filterExcelNameList_: str, nameSpace_: str):
        _excelToProtoStruct, _excelDataToProtoBin, _protoToPyClass, _protoToCsClass, _protoFolder, _binFolder, _pyCodeFolder, _csCodeFolder = self.stateToExcelToBin(nameSpace_)
        # --------------------------------------------------- 解析 excel 结构，生成 proto -------------------------------------------------------------------------
        _excelToProtoStruct.excelFolderToProtoFileRootList(dataCacheFolder_, excelFolder_, filterExcelNameList_, nameSpace_)  # 将 excel 转换成 protoRoot
        _excelToProtoStruct.protoRootListToProtoFiles(_protoFolder, filterExcelNameList_, nameSpace_)  # 将 protoRoot 转换成 .proto 文件
        # --------------------------------------------------- 根据 proto 生成 py ---------------------------------------------------------------------------------
        _protoToPyClass.protoFolderToPyClass(_protoFolder, _pyCodeFolder)  # 根据 proto 生成 py 文件
        # --------------------------------------------------- 根据 proto，解析 excel 数据，生成 bin  ---------------------------------------------------------------
        # 有缓存用缓存，没缓存用数据，使用pyClass的结构，将数据转换成bin文件，保存到承载bind的文件夹
        _excelDataToProtoBin.excelFolderDataToBin(dataCacheFolder_, excelFolder_, filterExcelNameList_, _pyCodeFolder, _binFolder, nameSpace_)
        # --------------------------------------------------- 根据 proto 生成 cs，解析 excel 数据 生成 cs 的配置入口，生成 cs 工程添加主入口文件 -----------------------
        # 通过 proto 生成 cs 代码
        _protoToCsClass.protoFolderToCsClass(_protoFolder, os.path.join(_csCodeFolder, "AutoCreateClass"))
        # 创建 CS 命令行工具 用来测试
        _protoToCsClass.createConsoleApp(_csCodeFolder, nameSpace_, dataCacheFolder_, excelFolder_, filterExcelNameList_, _binFolder)

    def excelFileToBin(self, dataCacheFolder_: str, excelFolder_: str, excelName_: str, nameSpace_: str):
        _excelToProtoStruct, _excelDataToProtoBin, _protoToPyClass, _protoToCsClass, _protoFolder, _binFolder, _pyCodeFolder, _csCodeFolder = self.stateToExcelToBin(nameSpace_)
        # --------------------------------------------------- 解析 excel 结构，生成 proto -------------------------------------------------------------------------
        _excelFile = self.getExcelFile(excelFolder_, excelName_)
        _excelToProtoStruct.excelFileToProtoFileRoot(dataCacheFolder_, _excelFile, nameSpace_)  # 将 excel 转换成 protoRoot
        _excelToProtoStruct.protoRootToProtoFile(_protoFolder, excelName_)  # 将 protoRoot 转换成 .proto 文件
        # --------------------------------------------------- 根据 proto 生成 py ---------------------------------------------------------------------------------
        _protoFile = self.getProtoFile(_protoFolder, excelName_)
        _protoToPyClass.protoFileToPyClass(_protoFolder, _protoFile, _pyCodeFolder)  # 根据 proto 生成 py 文件
        # --------------------------------------------------- 根据 proto，解析 excel 数据，生成 bin  ---------------------------------------------------------------
        # 有缓存用缓存，没缓存用数据，使用pyClass的结构，将数据转换成bin文件，保存到承载bind的文件夹
        _excelDataToProtoBin.excelFileDataToBin(dataCacheFolder_, _excelFile, _pyCodeFolder, _binFolder)
        # --------------------------------------------------- 根据 proto 生成 cs -----------------------
        _protoToCsClass.protoFileToCsClass(_protoFolder, _protoFile, os.path.join(_csCodeFolder, "AutoCreateClass"))


if __name__ == '__main__':
    from Main import Main
    from Proto.app.services.ProtoToClass.ProtoToClass import ProtoToClass
    from utils.CompanyUtil import Company_BB_Utils
    from BB.app.services.BBTs.BBTs_Config import BBTs_Config

    # 数据缓存路径
    _bbtsConfig: BBTs_Config = pyServiceUtils.getSubSvrByName("BB", "BBTs", "BBTs_Config")
    _dataCacheFolder = _bbtsConfig.subResPath
    # execl 文件路径
    _excelFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
    # 排除表
    _filterExcelNameList = ["RechargeMall", "RechargeGift", "UnitSkill", "Goddess"]
    # 命名空间
    _nameSpace = "ExcelConfig"

    # excel 数据 protobuf 格式化后，存入 bin 文件
    _main = Main()
    _proto: ProtoApp = _main.getAppByName("Proto")
    _proto.excelFolderToBin(_dataCacheFolder, _excelFolder, _filterExcelNameList, _nameSpace)
    _proto.excelFileToBin(_dataCacheFolder, _excelFolder, "Card", _nameSpace)
