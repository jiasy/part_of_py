#!/usr/bin/env python3
# Created by nobody at 2024/1/18
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import printUtils
from utils import fileUtils
from utils import folderUtils

import re
import os


class ProtoImportInfo(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(ProtoImportInfo, self).create()

    def destroy(self):
        super(ProtoImportInfo, self).destroy()

    # 获取 protoFolder_ 名称为 protoName_ 的 proto 文件的引用有哪些？
    def getImportProtoNameList(self, protoFolder_: str, protoName_: str):
        # 读取所有文件路径
        _protoPathDict = folderUtils.getFilePathKeyValue(protoFolder_, [".proto"])
        # 判断目标是否存在
        _targetProtoName = f'{protoName_}.proto'
        if _targetProtoName not in _protoPathDict:
            printUtils.pError(f"{_targetProtoName} 不在当期那文件夹中 ")
            sys.exit(1)
        # 读取目标内容，获取其引用的Proto
        _relativeProtoList = []
        _protoPath = _protoPathDict[_targetProtoName]
        self.getRelativeProto(_protoPath, _protoPathDict, _relativeProtoList)
        return _relativeProtoList

    # 分析文件内容将涉及的 proto 记录到 relativeProtoList_ 中
    def getRelativeProto(self, protoFilePath_: list, protoPathDict_: dict, relativeProtoList_: list):
        if not os.path.exists(protoFilePath_):
            printUtils.pError(f"{protoFilePath_} 不存在")
            sys.exit(1)
        _lines = fileUtils.linesFromFile(protoFilePath_)  # 读取内容
        for _idx in range(len(_lines)):
            _lastReg = re.search(r'\s*import\s+.*?\/?([a-zA-Z0-9_]+)\.proto', _lines[_idx])
            if _lastReg:
                _protoName = _lastReg.group(1)
                if _protoName not in relativeProtoList_:
                    relativeProtoList_.append(_protoName)  # 记录其引用的Proto
                    _targetProtoName = f'{_protoName}.proto'
                    if _targetProtoName not in protoPathDict_:
                        printUtils.pError(f"{_targetProtoName} 不在当期那文件夹中 ")
                        sys.exit(1)
                    _protoPath = protoPathDict_[_targetProtoName]  # 获取引用的Proto路径
                    self.getRelativeProto(_protoPath, protoPathDict_, relativeProtoList_)  # 将其也解析获取其相关的引用


if __name__ == '__main__':
    _protoImportInfo: ProtoImportInfo = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_protoImportInfo.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils

    _relativeProtoList = _protoImportInfo.getImportProtoNameList(Company_BB_Utils.getSLGProtobufFolderPath(), "Slg")
    print('_relativeProtoList = ' + str(_relativeProtoList))
