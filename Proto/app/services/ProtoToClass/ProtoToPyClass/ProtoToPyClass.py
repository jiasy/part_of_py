#!/usr/bin/env python3
# Created by nobody at 2023/12/11
from Proto.app.services.ExcelToProtoStruct.ExcelToProtoStruct import ExcelToProtoStruct
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import folderUtils
from utils import cmdUtils
import os

_folderPath = os.path.dirname(os.path.realpath(__file__))  # 当前执行目录


class ProtoToPyClass(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(ProtoToPyClass, self).create()

    def destroy(self):
        super(ProtoToPyClass, self).destroy()

    # protoFolder_ 的 proto 的根文件夹
    # protoFile_ 要生成代码的 proto 文件
    # pyCodeFolder_ 为生成代码的位置
    def getPyProtocCmd(self, protoFolder_: str, protoFile_: str, pyCodeFolder_: str):
        _cmd = f"protoc {protoFile_}"
        _cmd = f"{_cmd} -I={protoFolder_}"  # proto 的根目录，以便可以查找当期proto文件内所以引用的其他文件
        _cmd = f"{_cmd} --python_out {pyCodeFolder_}"
        return _cmd

    # 转换指定文件夹
    def protoFolderToPyClass(self, protoFolder_: str, pyCodeFolder_: str):
        from Proto.ProtoApp import ProtoApp
        _app: ProtoApp = self.app
        _protoFileDict = _app.getProtoFileDict(protoFolder_)
        for _protoFileName in _protoFileDict:
            _protoFile = _protoFileDict[_protoFileName]
            self.protoFileToPyClass(protoFolder_, _protoFile, pyCodeFolder_)

    # 转换指定文件
    def protoFileToPyClass(self, protoFolder_: str, protoFile_: str, pyCodeFolder_: str):
        _cmd = self.getPyProtocCmd(protoFolder_, protoFile_, pyCodeFolder_)
        cmdUtils.doStrAsCmd(_cmd, protoFolder_)


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr: ProtoToPyClass = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    # proto 结构定义文件
    _excelToProtoStruct: ExcelToProtoStruct = pyServiceUtils.getSvrByName("Proto", "ExcelToProtoStruct")

    _nameSpace = "ExcelConfig"
    # py 文件路径
    _pyCodeFolder = os.path.join(_subSvr.subResPath, _nameSpace)
    folderUtils.makeSureDirIsExists(_pyCodeFolder)

    # proto 文件
    _protoFolder = os.path.join(_excelToProtoStruct.resPath, _nameSpace)

    # 根据 proto 生成 py 文件
    _subSvr.protoFolderToPyClass(_protoFolder, _pyCodeFolder)
