#!/usr/bin/env python3
import os.path
from BB.app.services.BBTs.BBTs_Config import BBTs_Config
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import excelDataUtils
from utils import printUtils
from utils import folderUtils
from utils import fileUtils
from utils.excelDataUtils import DataCol
from utils.excelDataUtils import DataType
import importlib.util
import sys


class ExcelDataToProtoBin(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(ExcelDataToProtoBin, self).create()

    def destroy(self):
        super(ExcelDataToProtoBin, self).destroy()

    # 保存成 bin 文件
    @staticmethod
    def saveDataToBin(excelDataAsPb_, binPath_: str):
        _serializedData = excelDataAsPb_.SerializeToString()
        with open(binPath_, 'wb') as _file:
            _file.write(_serializedData)

    # 读取 bin 文件
    @staticmethod
    def loadDataFromBin(ExcelClass_, binPath_: str):
        with open(binPath_, 'rb') as _file:  # 从文件读取二进制数据
            _serializedData = _file.read()
        _excelDataAsPb = ExcelClass_()
        _excelDataAsPb.ParseFromString(_serializedData)
        return _excelDataAsPb

    # 根据名称获取运行时模块
    @staticmethod
    def getExcelPyModule(pyCodeFolder_: str, excelName_: str):
        # SAMPLE - 运行时，通过 py 路径加载模块
        _moduleName: str = f"{excelName_}_pb2"
        if _moduleName in sys.modules:
            return sys.modules[_moduleName]  # 曾经有过就返回
        _modulePath = os.path.join(pyCodeFolder_, f'{_moduleName}.py')  # py文件路径
        _spec = importlib.util.spec_from_file_location(_moduleName, _modulePath)
        _module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        sys.modules[_moduleName] = _module  # 记录模块
        return _module  # 并返回

    # 将每一行数据转换成 pb 对象
    @staticmethod
    def getCfgAsPbList(_cfgList: list[dict], StructClass_, fieldDataColDict_: dict[str:DataCol], IntListClass_, StrListClass_) -> list:
        _cfgAsPbList = []
        for _idx in range(len(_cfgList)):
            _cfg = _cfgList[_idx]  # 逐行数据
            _cfgAsPb = StructClass_()  # 创建每一行的 pb 数据承载对象
            for _fieldName in fieldDataColDict_:  # 逐个字段
                _fieldValue = _cfg[_fieldName]
                _dataCol: DataCol = fieldDataColDict_[_fieldName]
                if _dataCol.FieldType == DataType.Int:
                    setattr(_cfgAsPb, _fieldName, _fieldValue)
                elif _dataCol.FieldType == DataType.IntArr:
                    _repeatedFieldValue = getattr(_cfgAsPb, _fieldName)
                    _repeatedFieldValue.extend(_fieldValue)  # 直接连接数组
                elif _dataCol.FieldType == DataType.IntArrArr:
                    _repeatedFieldValue = getattr(_cfgAsPb, _fieldName)
                    _inArrArr: list[list[int]] = _fieldValue
                    for _idxArrArr in range(len(_inArrArr)):
                        _intList = IntListClass_()  # 创建二级列表
                        _intList.value.extend(_inArrArr[_idxArrArr])
                        _repeatedFieldValue.append(_intList)  # 汇总二维数组
                elif _dataCol.FieldType == DataType.Str:
                    setattr(_cfgAsPb, _fieldName, _fieldValue)
                elif _dataCol.FieldType == DataType.StrArr:
                    _repeatedFieldValue = getattr(_cfgAsPb, _fieldName)
                    _repeatedFieldValue.extend(_fieldValue)  # 直接连接数组
                elif _dataCol.FieldType == DataType.StrArrArr:
                    _repeatedFieldValue = getattr(_cfgAsPb, _fieldName)
                    _strArrArr: list[list[str]] = _fieldValue
                    for _idxArrArr in range(len(_strArrArr)):
                        _strList = StrListClass_()  # 创建二级列表
                        _strList.value.extend(_strArrArr[_idxArrArr])
                        _repeatedFieldValue.append(_strList)  # 汇总二维数组
            _cfgAsPbList.append(_cfgAsPb)  # 记录这一条数据
        return _cfgAsPbList

    # excel 文件夹 pb 格式的文件
    def excelFolderDataToBin(self, dataCacheFolder_: str, excelFolder_: str, filterExcelNameList_: str, pyCodeFolder_: str, binFolder_: str, nameSpace_: str):
        from Proto.ProtoApp import ProtoApp
        _app: ProtoApp = self.app
        _excelFileDict = _app.getExcelFileDict(excelFolder_)
        _pyFileDict = _app.getPyFileDict(pyCodeFolder_)

        for _excelName in _excelFileDict:
            if _excelName in filterExcelNameList_:
                continue
            if _excelName == nameSpace_:
                print(f"ERROR : {nameSpace_} 为命名的 excel 无法生成")
                sys.exit(1)
            _excelFile = _excelFileDict[_excelName]  # 文件路径
            self.excelFileDataToBin(dataCacheFolder_, _excelFile, pyCodeFolder_, binFolder_)

    # excel 文件转 bin
    def excelFileDataToBin(self, dataCacheFolder_: str, excelFile_: str, pyCodeFolder_: str, binFolder_: str):
        _excelName = fileUtils.justName(excelFile_)
        _module = self.getExcelPyModule(pyCodeFolder_, _excelName)  # xx_pb2 模块
        _dataSheetDict, _fieldDataColDictDict = excelDataUtils.getCacheExcelData(dataCacheFolder_, excelFile_)  # 数据结构获取
        _ExcelClass = getattr(_module, f'{_excelName}Root')  # excel 全部页面的数据
        _excelDataAsPb = _ExcelClass()  # 创建 Excel 的 pb 数据承载对象
        for _structName in _dataSheetDict:  # 缓冲数据中，每一个 sheet 页面的结构
            _StructClass = getattr(_module, _structName)  # 获取结构类
            _IntListClass = getattr(_module, f'{_excelName}IntList')  # 获取可能的二维数组支持
            _StrListClass = getattr(_module, f'{_excelName}StrList')

            _cfgList: list[dict] = _dataSheetDict[_structName]  # 获取页面数据
            _fieldDataColDict: dict[str:DataCol] = _fieldDataColDictDict[_structName]  # 页面列信息
            _cfgAsPbList = self.getCfgAsPbList(_cfgList, _StructClass, _fieldDataColDict, _IntListClass, _StrListClass)

            _repeatedAttr = getattr(_excelDataAsPb, _structName)
            _repeatedAttr.extend(_cfgAsPbList)  # 数据列表添加的根节点

        # 保存 Excel 根节点成 bin 文件
        _binPath = os.path.join(binFolder_, f"{_excelName}.bin")
        self.saveDataToBin(_excelDataAsPb, _binPath)
        del _excelDataAsPb

    # 打印 bin 内容，越来越慢？
    def binFolderPrint(self, pyCodeFolder_: str, binFolder_: str):
        from Proto.ProtoApp import ProtoApp
        _app: ProtoApp = self.app
        _binFileDict = _app.getBinFileDict(binFolder_)
        for _binName in _binFileDict:
            _binPath = os.path.join(binFolder_, f"{_binName}.bin")
            _module = self.getExcelPyModule(pyCodeFolder_, _binName)  # xx_pb2 模块
            _ExcelClass = getattr(_module, f'{_binName}Root')  # excel 全部页面的数据
            _excelDataAsPbRead = self.loadDataFromBin(_ExcelClass, _binPath)
            printUtils.pTitleLog(_binName, " ---------------------------------------------- ")
            print(_excelDataAsPbRead)
            del _excelDataAsPbRead


if __name__ == '__main__':
    _svr: ExcelDataToProtoBin = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
    from Proto.app.services.ProtoToClass.ProtoToPyClass import ProtoToPyClass
    from utils.CompanyUtil import Company_BB_Utils

    _nameSpace = "ExcelConfig"

    # 生成代码位置
    _protoToPyClass: ProtoToPyClass = pyServiceUtils.getSubSvrByName("Proto", "ProtoToClass", "ProtoToPyClass")
    _pyCodeFolder = os.path.join(_protoToPyClass.subResPath, _nameSpace)

    # excel 位置，用来获取数据
    _excelFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
    # 排除表
    _filterExcelNameList = ["RechargeMall", "RechargeGift", "UnitSkill", "Goddess"]
    # 数据缓存位置
    _bbtsConfig: BBTs_Config = pyServiceUtils.getSubSvrByName("BB", "BBTs", "BBTs_Config")
    # bin 文件保存的位置
    _binFolder = os.path.join(_svr.resPath, _nameSpace)
    folderUtils.makeSureDirIsExists(_binFolder)

    # 有缓存用缓存，没缓存用数据，使用pyClass的结构，将数据转换成bin文件，保存到承载bind的文件夹
    _svr.excelFolderDataToBin(_bbtsConfig.subResPath, _excelFolder, _filterExcelNameList, _pyCodeFolder, _binFolder, _nameSpace)

    # 打印 bin 文件夹内容
    _svr.binFolderPrint(_pyCodeFolder, _binFolder)
