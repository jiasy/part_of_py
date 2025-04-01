import xlwings as xw

import json
import subprocess

from utils import strUtils
from utils import fileUtils
import os
from enum import Enum
import pickle


class DataType(Enum):
    # 删


class DataCol:
    def __init__(self):
        self.cnName = None  # 中文名/描述
        self.FieldName = None  # 名称
        self.FieldType = DataType.NONE  # 类型
        self.Default = None  # 默认值
        self.values = []  # 每一行的值
        self.colId = None  # 数据所在的列


def getMatrixDict(excelPath_: str):
    _app = xw.App()
    # 打开Excel文件并禁用宏警告提示
    _wb = xw.Book(excelPath_, update_links=False, read_only=True)
    _sheetNameToMatrixDict = {}
    for _sheet in _wb.sheets:
        _sheetName = _sheet.name  # 获取工作表名称
        _dataRange = _sheet.used_range  # 获取数据范围
        _rowMax = _dataRange.rows.count  # 获取行数和列数
        _colMax = _dataRange.columns.count
        if _dataRange.value is None:
            print(f"    {excelPath_} - {_sheetName} : data is none")
            continue
        _matrix = []  # 创建空的行列式数据结构
        # 逐行读取Excel数据并重组为行列式格式
        for _row in _dataRange.value:
            _matrix.append(_row)
        _sheetNameToMatrixDict[_sheetName] = _matrix
    # 关闭Excel文件并退出应用
    _wb.close()
    _app.quit()
    return _sheetNameToMatrixDict


def printContent(matrixDict_: dict, key_: str):
    _matrix = matrixDict_[key_]
    rowMax = len(_matrix)
    colMax = len(_matrix[0])
    _cId = 0
    while _cId < colMax:
        _cId = _cId + 1
        if _cId == 1:
            continue  # 第一列没用
        _rId = 0
        # 每一列数据
        while _rId < rowMax:
            _rId = _rId + 1
            print(f"[{_rId - 1},{_cId - 1}] : {_matrix[_rId - 1][_cId - 1]}")


def toDictList(matrixDict_: dict, sheetName_):
    # 删
    return _dataList, _fieldNameToDataColDict


def toData(matrixDict_):
    _dataSheetDict = {}  # 数据信息
    _fieldDataColDictDict = {}  # 字段对象
    for _sheetName in matrixDict_:
        if strUtils.isValidCodeName(_sheetName):  # 合法的名称才会被转换成数据保存
            _dataList, _fieldNameToDataColDict = toDictList(matrixDict_, _sheetName)
            if len(_dataList) > 0:  # 没有数据就不记录
                _dataSheetDict[_sheetName] = _dataList
                _fieldDataColDictDict[_sheetName] = _fieldNameToDataColDict
    return _dataSheetDict, _fieldDataColDictDict


# 取值
def getValue(dataCol_, value_):
    # 删


# 取实际值
def getRealValue(dataCol_, value_):
    _backValue = None
    if value_ is None:  # 没有值就给默认值
        _backValue = dataCol_.Default
    else:
        _backValue = getValue(dataCol_, value_)
    return _backValue


# 取默认值
def getDefault(dataCol_, value_):
    # 删


# 获取类别
def getType(fieldName_: str, typeStr_: str):
    # 删
    return DataType.NONE


# 获取文件的第一行
def getFirstLine(filePath_):
    command = f"head -n 1 {filePath_}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    first_line = result.stdout.strip()
    return first_line


# 获取除第一行之外的所有内容
def getLinesExceptFirstLine(filePath_):
    command = f"tail -n +2 {filePath_}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    content_except_first_line = result.stdout.strip()
    return content_except_first_line


# 获取数据
def getCacheExcelData(folderPath_: str, excelFile_: str):
    _excelName = fileUtils.justName(excelFile_)
    _dataCacheFile = os.path.join(folderPath_, _excelName, f"{_excelName}.json")
    _dataStructCacheFile = os.path.join(folderPath_, _excelName, f"{_excelName}_struct.pkl")
    _needWriteToJson = False  # 需要写缓存
    _curMd5 = fileUtils.calculate_md5(excelFile_)  # 当前的 md5
    if os.path.exists(_dataCacheFile):  # 有缓存比较其内容
        _saveMd5 = getFirstLine(_dataCacheFile)  # 以前存的 md5
        if _curMd5 != _saveMd5:  # 有修改
            _needWriteToJson = True
    else:  # 没存过
        _needWriteToJson = True
    # 需要写缓存
    if _needWriteToJson:
        _sheetNameToMatrixDict = getMatrixDict(excelFile_)
        _dataSheetDict, _fieldDataColDictDict = toData(_sheetNameToMatrixDict)
        fileUtils.writeFileWithStr(_dataCacheFile, f'{_curMd5}\n' + str(json.dumps(_dataSheetDict, indent=4, sort_keys=False, ensure_ascii=False)))
        # SAMPLE - pkl dump 对象成文件
        with open(_dataStructCacheFile, 'wb') as _pklFile:
            pickle.dump(_fieldDataColDictDict, _pklFile)
        print(f'Read - {excelFile_}')
    else:
        print(f'- cache - {excelFile_}')

    # 从文件反序列化字典
    with open(_dataStructCacheFile, 'rb') as _pklFile:
        _fieldDataColDictDict = pickle.load(_pklFile)
    # 读取缓存
    _dataSheetDict = json.loads(getLinesExceptFirstLine(_dataCacheFile))
    return _dataSheetDict, _fieldDataColDictDict
