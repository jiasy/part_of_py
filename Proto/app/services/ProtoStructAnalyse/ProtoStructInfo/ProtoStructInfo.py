# !/usr/bin/env python3
# Created by nobody at 2019/3/4
from base.supports.Base.BaseInService import BaseInService
from utils import folderUtils
from utils import fileUtils
import re
from utils import pyServiceUtils
import os
from utils import strUtils
import sys
from utils import printUtils


class ProtoStructInfo(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(ProtoStructInfo, self).create()

    def destroy(self):
        super(ProtoStructInfo, self).destroy()

    # 解析 .proto 文件
    def getProtobufStructInfoDict(self, protoFolderPath_):
        _protoStructInfoDict = {}
        _filePathDict = folderUtils.getFilePathKeyValue(protoFolderPath_, [".proto"])
        for _k, _v in _filePathDict.items():
            _keyName = _k.split("/")[-1].split(".")[0]
            # 名称 -> 路径 关系输出
            # print(str(_keyName).ljust(15) + ":" + str(_v))
            _currentProtoInfo = self.getProtobufStructInfo(_keyName, _v)
            _protoStructInfoDict[_keyName] = _currentProtoInfo
            # 输出 proto 结构信息
            # print(str(json.dumps(_currentProtoInfo, indent=4, sort_keys=False, ensure_ascii=False)))
            # 输出 proto 结构的 json 结构样式
            # dictUtils.showDictStructure(_currentProtoInfo)
        return _protoStructInfoDict

    # 整理字符串格式
    def formatProtoStr(self, protoStr_: str):
        _protoStr = protoStr_
        # 整理空格行
        regex = r"\n(\s*)\n"
        while re.search(regex, _protoStr):
            _protoStr = re.sub(regex, r'\n', _protoStr)

        # 移除空白行
        regex = r"\n\n"
        while re.search(regex, _protoStr):
            _protoStr = re.sub(regex, r'\n', _protoStr)

        # 删

        # 移除空白行
        regex = r"\n\n"
        while re.search(regex, _protoStr):
            _protoStr = re.sub(regex, r'\n', _protoStr)

        return _protoStr

    # 去除非结构字符串
    def removeUnuseStr(self, protocolStr_):
        # 删

    # 去除注释
    def removeComment(self, protocolStr_: str):
        _lines = protocolStr_.split("\n")
        for _i in range(len(_lines)):
            _lines[_i] = _lines[_i].split("//")[0].strip()
        return "\n".join(_lines)

    # 去除属性注释的空白间隔
    def removePropertyCommentSpace(self, protocolStr_: str):
        _protoStr = protocolStr_
        regex = r";.*//(.*)\n"
        _protoStr = re.sub(regex, r';//\1\n', _protoStr)
        return _protoStr

    # 重新构建protobuf字符串结构，将嵌套部分提出来然后重新命名
    def reStructProtoStr(self, protocolStr_: str):
        # 删

    # 移除多行注释
    def removeMutiltyCommon(self, content_):
        _strList = strUtils.splitByList(content_, ["/**", "/*", "*/"])
        _newStr = ""
        for _idx in range(len(_strList)):
            if _idx % 2 == 0:
                _newStr = _newStr + _strList[_idx]
        return _newStr

    '''
    SAMPLE - protobuf 解析使用的 json 结构
    解析 protobuf ，返回这样的结构
    '''

    # 解析 protobuf 文件，生成对应的 json 结构，用来记录 protobuf 的结构信息
    def getProtobufStruct(self, protoFilePath_: str):
        return self.getProtobufStructInfo(os.path.basename(protoFilePath_), protoFilePath_)

    def getProtobufStructInfo(self, keyName_: str, protoFilePath_: str):
        # 删
        return _currentProto

    # 打印一个 proto 文件的结构
    def printProtoInfo(self, protoFilePath_: str):
        _protoInfo = self.getProtobufStruct(protoFilePath_)
        _protoName = fileUtils.justName(protoFilePath_)
        printUtils.printPyObjAsKV(_protoName, _protoInfo)


if __name__ == "__main__":
    pyServiceUtils.printSubSvrCode(__file__)
    _subSvr: ProtoStructInfo = pyServiceUtils.getSubSvr(__file__)
    _protoFilePath = "/disk/SY/protocol_farm/server/dailyTask/TakeTaskAwardRes.proto"
    _subSvr.printProtoInfo(_protoFilePath)
