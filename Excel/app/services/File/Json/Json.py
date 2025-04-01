#!/usr/bin/env python3
# Created by nobody at 2020/9/9
from utils import folderUtils
from utils import sysUtils
from utils import jsonUtils
from utils import fileUtils
from utils import dataSetUtils
import os
import json
import sys

from Excel.ExcelBaseInService import ExcelBaseInService


class Json(ExcelBaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.funcDict = {
            "MargeJsonDict": {
                "toJsonFilePath": "要合并的 json 文件路径",
                "margeJsonDict": "需要合并的 json 结构 ，使用 DictSheet 的格式 进行配置",
            },
            "MargeJsonFile": {
                "fromJsonFilePath": "从哪个 json 文件路径来",
                "toJsonFilePath": "需要合并到哪个 json 文件中去",
            },
            "WriteJsonFile": {
                "toJsonFilePath": "写入的 json 文件路径",
                "jsonDict": "需要写入的 json 内容 ，使用 DictSheet 的格式 进行配置",
            },
            "DiffJsonFile": {
                "oldJsonFilePath": "老文件",
                "newJsonFilePath": "新文件",
                "diffJsonFilePath": "标结果文件",
            },
        }

    def create(self):
        super(Json, self).create()

    def destroy(self):
        super(Json, self).destroy()

    # 合并文件json内容
    def MargeJsonFile(self, dParameters_: dict):
        _toJsonFilePath = dParameters_["toJsonFilePath"]
        _fromJsonFilePath = dParameters_["fromJsonFilePath"]
        _jsonDict = fileUtils.dictFromJsonFile(_toJsonFilePath)
        _margeJsonDict = fileUtils.dictFromJsonFile(_fromJsonFilePath)
        _jsonDict = jsonUtils.mergeAToB(_margeJsonDict, _jsonDict)  # 合并
        fileUtils.writeFileWithStr(  # 写回去
            _toJsonFilePath,
            str(json.dumps(_jsonDict, indent=4, sort_keys=False, ensure_ascii=False))
        )

    # 比较Json内容得到不一样的
    def DiffJsonFile(self, dParameters_: dict):
        _oldJsonFilePath = dParameters_["oldJsonFilePath"]
        _newJsonFilePath = dParameters_["newJsonFilePath"]
        _diffJsonFilePath = dParameters_["diffJsonFilePath"]
        _oldDict = fileUtils.dictFromJsonFile(_oldJsonFilePath)
        _newDict = fileUtils.dictFromJsonFile(_newJsonFilePath)

        _dataSetCache = {}
        _oldChangeList = dataSetUtils.setValueToDataPath("old", _oldDict, _dataSetCache)
        _newChangeList = dataSetUtils.setValueToDataPath("new", _newDict, _dataSetCache)

        # 去掉路径中的 old. 和 new.，使得后面保持一致
        for _i in range(len(_oldChangeList)):
            _oldChangeList[_i] = _oldChangeList[_i][4:]
        for _i in range(len(_newChangeList)):
            _newChangeList[_i] = _newChangeList[_i][4:]

        # 并集 - 交集 得到不同路径
        _justInNewSet = set(set(_newChangeList) - set(_oldChangeList))
        _justInNewList = list(_justInNewSet)
        for _i in range(len(_justInNewList)):
            _justInNewPath = _justInNewList[_i]
            dataSetUtils.setValueToDataPath(
                "diff." + _justInNewPath,  # 放置到不同路径中
                dataSetUtils.getValueByDataPath("new." + _justInNewPath, _dataSetCache),  # 新数据中的内容
                _dataSetCache
            )

        # 交集部分中不同的
        _intersectionList = list(set(set(_newChangeList) & set(_oldChangeList)))
        for _i in range(len(_intersectionList)):
            _intersectionElement = _intersectionList[_i]
            _oldValue = dataSetUtils.getValueByDataPath("old." + _intersectionElement, _dataSetCache)
            _newValue = dataSetUtils.getValueByDataPath("new." + _intersectionElement, _dataSetCache)
            # 比较值
            if not _oldValue == _newValue:
                dataSetUtils.setValueToDataPath(
                    "diff." + _intersectionElement,  # 放置到不同路径中
                    _newValue,
                    _dataSetCache
                )

        fileUtils.writeFileWithStr(  # 写回去
            _diffJsonFilePath,
            str(
                json.dumps(
                    dataSetUtils.dataSetToJsonDict("diff", _dataSetCache),
                    indent=4, sort_keys=False, ensure_ascii=False
                )
            )
        )

    # 用内容合文件
    def MargeJsonDict(self, dParameters_: dict):
        _toJsonFilePath = dParameters_["toJsonFilePath"]
        _margeJsonDict = dParameters_["margeJsonDict"]
        _jsonDict = fileUtils.dictFromJsonFile(_toJsonFilePath)
        _jsonDict = jsonUtils.mergeAToB(_margeJsonDict, _jsonDict)  # 合并
        fileUtils.writeFileWithStr(  # 写回去
            _toJsonFilePath,
            str(json.dumps(_jsonDict, indent=4, sort_keys=False, ensure_ascii=False))
        )

    # 用内容写文件
    def WriteJsonFile(self, dParameters_: dict):
        _toJsonFilePath = dParameters_["toJsonFilePath"]
        _jsonDict = dParameters_["jsonDict"]
        fileUtils.writeFileWithStr(  # 写回去
            _toJsonFilePath,
            str(json.dumps(_jsonDict, indent=4, sort_keys=False, ensure_ascii=False))
        )


import Main

if __name__ == "__main__":
    # 直接复制，到新文件中，只需要改，所需参数 和 命令行参数
    _folderPath = os.path.dirname(os.path.realpath(__file__))  # 当前执行目录
    _folderSplit = os.path.split(_folderPath)  # 切目录
    _baseServiceName = os.path.split(_folderSplit[0])[1]  # 再切得到上一层文件夹名
    _subBaseInServiceName = _folderSplit[1]  # 切到的后面就是子服务名称

    # _functionName = "MargeJsonDict"
    # _parameterDict = {  # 所需参数
    #     "toJsonFilePath": "{resFolderPath}/jsconfig.json",
    #     "margeJsonDict": {
    #         "exclude": [
    #             "node_modules",
    #             ".vscode",
    #             "library",
    #             "local",
    #             "settings",
    #             "temp"
    #         ],
    #         "compilerOptions": {
    #             "addParameter": "added",  # 添加一个参数
    #             "target": "es5"  # 修改一个参数
    #         }
    #     }
    # }

    # _functionName = "WriteJsonFile"
    # _parameterDict = {  # 所需参数
    #     "toJsonFilePath": "{resFolderPath}/createJson.json",
    #     "jsonDict": {
    #         "exclude": [
    #             "node_modules",
    #             ".vscode",
    #             "library",
    #             "local",
    #             "settings",
    #             "temp"
    #         ],
    #         "compilerOptions": {
    #             "addParameter": "added",
    #             "target": "es5"
    #         }
    #     }
    # }

    # _functionName = "MargeJsonFile"
    # _parameterDict = {  # 所需参数
    #     "fromJsonFilePath": "{resFolderPath}/createJson.json",
    #     "toJsonFilePath": "{resFolderPath}/jsconfig.json",
    # }

    _functionName = "DiffJsonFile"
    _parameterDict = {  # 所需参数
        "oldJsonFilePath": "{resFolderPath}/diff/a.json",
        "newJsonFilePath": "{resFolderPath}/diff/b.json",
        "diffJsonFilePath": "{resFolderPath}/diff/diff.json",
    }

    Main.excelProcessStepTest(
        _baseServiceName,
        _subBaseInServiceName,
        _functionName,
        _parameterDict,
        {  # 命令行参数
            "executeType": "单体测试"
        }
    )

    Main.execExcelCommand(
        _baseServiceName,
        _subBaseInServiceName,
        _functionName,
        {  # 命令行参数
            "executeType": "单体测试"
        }
    )
