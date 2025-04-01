import sys

from utils import pyServiceUtils
from utils import folderUtils
from utils import fileUtils
from utils import strUtils
import xlwings as xw
import os
from utils import fileSystemCacheUtils


def getConstructStr(fieldName_: str, common_: str):
    if fieldName_ == "Id":
        return ""
    return f'''        cls._{fieldName_}_value = None  # {common_}
        cls._{fieldName_}_mark = False'''


def getConstructListStr(fieldNameList_: list, commonList_: list):
    _constructListStr = ""
    for _i in range(len(fieldNameList_)):
        _constructListStr = _constructListStr + getConstructStr(fieldNameList_[_i], commonList_[_i]) + "\n"
    return _constructListStr


def getReadOnlyStr(fieldName_: str):
    if fieldName_ == "Id":
        return ""
    return f'''
    @property
    def {fieldName_}(cls):
        return cls._{fieldName_}_value

    @{fieldName_}.setter
    def {fieldName_}(cls, value_):
        if not cls._{fieldName_}_mark:
            cls._{fieldName_}_value = value_
            cls._{fieldName_}_mark = True
        else:
            raise AttributeError("Cannot modify read-only variable")
'''


def getReadOnlyListStr(fieldNameList_: list):
    _readOnlyListStr = ""
    for _i in range(len(fieldNameList_)):
        _readOnlyListStr = _readOnlyListStr + getReadOnlyStr(fieldNameList_[_i]) + "\n"
    return _readOnlyListStr


def getInitStr(fieldName_: str):
    if fieldName_ == "Id":
        return ""
    return f'        cls.{fieldName_} = cfg_.get("{fieldName_}")'


def getInitListStr(fieldNameList_: list):
    _initListStr = ""
    for _i in range(len(fieldNameList_)):
        _initListStr = _initListStr + getInitStr(fieldNameList_[_i]) + "\n"
    return _initListStr


def getToDictStr(fieldName_: str):
    if fieldName_ == "Id":
        return ""
    return f'        _dict["{fieldName_}"] = cls.{fieldName_}'


def getToDictListStr(fieldNameList_: list):
    _toDictListStr = ""
    for _i in range(len(fieldNameList_)):
        _toDictListStr = _toDictListStr + getToDictStr(fieldNameList_[_i]) + "\n"
    return _toDictListStr


# 创建 Sheet 代码
def createSheetClass(sheetName_: str, fieldNameList_: list, commonList_: list):
    # 删


# 创建 Excel 代码
def createExcelClass(excelName_: str, classFolderPath_: str, sheetNameList_: str):
    # 删


# 创建 ExcelBase 代码
def createExcelBaseClass(excelToSheetListDict_: dict):
    # 删


def createConfigClasses(excelPath_: str, excelName_: str, classFolderPath_: str):
    print(f"    Excel : {excelName_}")
    folderUtils.makeSureDirIsExists(os.path.join(classFolderPath_, excelName_))
    # 创建每一个Sheet对应的类
    wb = xw.Book(excelPath_, update_links=False, read_only=True)
    _matrixDict = {}
    _sheetNameList = []
    for _sheet in wb.sheets:
        _sheetName = _sheet.name  # 获取工作表名称
        if not strUtils.isValidCodeName(_sheetName):
            print(f'        - {_sheetName} is not valid name')
            continue
        _dataRange = _sheet.used_range  # 获取数据范围
        _colMax = _dataRange.columns.count
        if _dataRange.value is None:
            print(f'        - {_sheetName} no data...')
            continue
        _rowZero = _dataRange.value[0]
        _rowOne = _dataRange.value[1]
        _rowTwo = _dataRange.value[2]
        if _rowTwo[0] != "FieldType" or _rowOne[0] != "FieldName":
            print(f'        - {_sheetName} is not data struct')
            continue
        print(f"        Sheet : {_sheetName}")
        _fieldNameList = []
        _commonList = []
        for _col in range(_colMax):
            if _col == 0:
                continue
            _fieldName = _rowOne[_col]
            if _fieldName is not None and isinstance(_fieldName, str):
                _fieldName = _fieldName.strip()
                if strUtils.isValidCodeName(_fieldName):
                    _fieldNameList.append(_fieldName)
                    _commonList.append(_rowZero[_col])
        # 创建代码
        _fieldNameList = list(set(_fieldNameList))
        _classStr = createSheetClass(_sheetName, _fieldNameList, _commonList)
        _classPath = os.path.join(classFolderPath_, excelName_, f"{_sheetName}_Sheet.py")
        fileUtils.writeFileWithStr(_classPath, _classStr)
        _sheetNameList.append(_sheetName)
    wb.close()
    # 创建 Excel 对应的类
    createExcelClass(excelName_, classFolderPath_, _sheetNameList)
    return _sheetNameList


if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    _filterExcelNameList = [
        "RechargeMall",
        "RechargeGift",
    ]

    from utils.CompanyUtil import Company_BB_Utils
    import os

    _classFolderPath = "/Users/XS/Documents/develop/GitHub/Services/PY_Service/XS/app/services/BBTs/BBTs_Config/ConfgClass"
    _excelFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
    _xlsxFilePathList = folderUtils.getFileListInFolder(_excelFolderPath, [".xlsm"])
    _excelToSheetListDict = {}
    _sheetNameToExcelNameDict = {}

    for _idx in range(len(_xlsxFilePathList)):
        _xlsxFilePath = _xlsxFilePathList[_idx]
        _excelName = fileUtils.justName(_xlsxFilePath)
        # if _excelName != "RechargeMall" and _excelName != "RechargeGift" and _excelName != "RechargeTier":
        #     continue
        if _excelName in _filterExcelNameList:  # 过滤的不解析
            continue
        if strUtils.isValidCodeName(_excelName):
            _sheetNameList = createConfigClasses(_xlsxFilePath, _excelName, _classFolderPath)
            _excelToSheetListDict[_excelName] = _sheetNameList
            # 名称排重
            for _sheetIdx in range(len(_sheetNameList)):
                _sheetName = _sheetNameList[_sheetIdx]
                if _sheetName in _sheetNameToExcelNameDict:
                    print(f"ERROR : sheet {_sheetName} 命名重复 {_sheetNameToExcelNameDict[_sheetName]} - {_excelName}")
                    sys.exit(1)
                _sheetNameToExcelNameDict[_sheetName] = _excelName
        # break

    # 生成综合基类
    fileUtils.writeFileWithStr(
        os.path.join(_classFolderPath, f"ConfigSheetBase.py"),
        createExcelBaseClass(_excelToSheetListDict)
    )
