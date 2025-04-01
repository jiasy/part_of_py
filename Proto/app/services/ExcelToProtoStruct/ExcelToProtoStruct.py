#!/usr/bin/env python3
import sys

from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import fileUtils
from utils import folderUtils
from utils import excelDataUtils
from BB.app.services.BBTs.BBTs_Config import BBTs_Config
from Proto.app.services.ExcelToProtoStruct.support.ProtoFileRoot import ProtoFileRoot
from utils.excelDataUtils import DataCol
import os

_folderPath = os.path.dirname(os.path.realpath(__file__))  # 当前执行目录


class ExcelToProtoStruct(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        self.protoFileRootDict: dict[str:ProtoFileRoot] = {}

    def create(self):
        super(ExcelToProtoStruct, self).create()

    def destroy(self):
        super(ExcelToProtoStruct, self).destroy()

    # 文件夹内的 excel，识别其结构，并转换成 DataCol 所能标示的列结构构成的数据
    def excelFolderToProtoFileRootList(self, dataCacheFolder_: str, excelFolder_: str, filterExcelNameList_: str, nameSpace_: str):
        from Proto.ProtoApp import ProtoApp
        _app: ProtoApp = self.app
        _excelFileDict = _app.getExcelFileDict(excelFolder_)
        for _excelName in _excelFileDict:
            if _excelName in filterExcelNameList_:
                continue
            _excelFile = _excelFileDict[_excelName]  # 文件路径
            self.excelFileToProtoFileRoot(dataCacheFolder_, _excelFile, nameSpace_)

    # 将一个文件转换成结构数据
    def excelFileToProtoFileRoot(self, dataCacheFolder_: str, excelFile_: str, nameSpace_: str):
        _excelName = fileUtils.justName(excelFile_)
        _protoRoot = ProtoFileRoot(nameSpace_, _excelName)  # proto 文件根节点
        _, _fieldDataColDictDict = excelDataUtils.getCacheExcelData(dataCacheFolder_, excelFile_)  # 数据结构获取
        for _sheetName in _fieldDataColDictDict:  # 每一个 sheet 页面
            _protoStruct = _protoRoot.addStruct(_sheetName)  # 每一个页面对应的结构对象
            _dataColDict: dict[str:DataCol] = _fieldDataColDictDict[_sheetName]  # 这个页面的数据结构
            for _paramName in _dataColDict:  # 每一个字段名
                _dataCol: DataCol = _dataColDict[_paramName]  # 每一个字段信息
                _protoStruct.addField(_dataCol)  # 为结构添加字段
        self.protoFileRootDict[_excelName] = _protoRoot

    # 将 py 结构文件生成到指定目录中
    def protoRootListToProtoFiles(self, protoFolder_: str, filterExcelNameList_: str, nameSpace_: str):
        for _excelName in self.protoFileRootDict:
            if _excelName in filterExcelNameList_:
                continue
            if _excelName == nameSpace_:
                print(f"ERROR : {nameSpace_} 为命名的 excel 生成")
                sys.exit(1)
            self.protoRootToProtoFile(protoFolder_, _excelName)

    # 根节点转换 proto 文件
    def protoRootToProtoFile(self, protoFolder_: str, excelName_: str):
        if excelName_ not in self.protoFileRootDict:
            print(f"ERROR : {excelName_} 不存在")
            sys.exit(1)
        _protoRoot: ProtoFileRoot = self.protoFileRootDict[excelName_]
        _protoFile = os.path.join(protoFolder_, f"{excelName_}.proto")
        fileUtils.writeFileWithStr(_protoFile, _protoRoot.toProtobufContent())
        print(f'    create : {_protoFile}')


if __name__ == '__main__':
    _svr: ExcelToProtoStruct = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils

    _bbtsConfig: BBTs_Config = pyServiceUtils.getSubSvrByName("BB", "BBTs", "BBTs_Config")

    _nameSpace = "ExcelConfig"

    # 生成的 proto 放置的文件目录
    _protoFolder = os.path.join(_svr.resPath, _nameSpace)
    folderUtils.makeSureDirIsExists(_protoFolder)

    # execl 文件路径
    _excelFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
    # 排除表
    _filterExcelNameList = ["RechargeMall", "RechargeGift", "UnitSkill", "Goddess"]
    # 将 excel 转换成 protoRoot
    _svr.excelFolderToProtoFileRootList(_bbtsConfig.subResPath, _excelFolder, _filterExcelNameList, _nameSpace)

    # 将 protoRoot 转换成 .proto 文件
    _svr.protoRootListToProtoFiles(_protoFolder, _filterExcelNameList, _nameSpace)
