# !/usr/bin/env python3
import os
import re
import logging
import sys

import utils.printUtils
from utils import fileUtils
from utils import listUtils
from utils import folderUtils


# targetProtoFolderPath_ 中获取 protoNameList_ 列表中的 文件，放置到 recoverProtoFolderPath_ 下 moduleName_ 文件夹内
def styleFrom3to2(targetProtoFolderPath_: str, moduleName_: str, protoNameList_: list, recoverProtoFolderPath_: str):
    if protoNameList_ == None or len(protoNameList_) == 0:
        print("        未指定任何 pb ,可能是使用其他已有结构")
        return
    for _idx in range(len(protoNameList_)):
        _protoName = protoNameList_[_idx]
        if _protoName.endswith(".proto"):
            utils.printUtils.pError("不必携带后缀 " + _protoName)
            sys.exit(1)

    # recoverProtoFolderPath_ 文件夹 还原
    _recoverModuleProtoFolder = os.path.join(recoverProtoFolderPath_, moduleName_)
    folderUtils.deleteThenCreateFolder(recoverProtoFolderPath_)  # 将文件夹还原

    # protoNameList_ 中，每一个 proto
    _protoFilePathList = folderUtils.getFileListInFolder(targetProtoFolderPath_, [".proto"])
    for _idx in range(len(_protoFilePathList)):
        _srcProtoPath = _protoFilePathList[_idx]
        _protoName = fileUtils.justName(_srcProtoPath)
        if _protoName in protoNameList_:  # 将每一个 protobuf 都 3 转 2
            _dstProtoPath = os.path.join(_recoverModuleProtoFolder, _protoName + ".proto")
            _newProtoContent = recoverProtoStyle(fileUtils.linesFromFile(_srcProtoPath))  # 读取并修改 proto 内容
            fileUtils.writeFileWithStr(_dstProtoPath, _newProtoContent)  # 写入 recover proto


# 实际上 2 和 3 的差距不大，就是 optional 关键字没有了，3 全部都是 optional
def recoverProtoStyle(protoLines_: list):
    _newLines = []
    for _i in range(len(protoLines_)):
        _line = protoLines_[_i].replace("\n", "")
        _reg = re.search(
            # "    repeated 或 空           自定义结构/int32          属性名                  = 16;"
            r'[\t|\s]*(repeated[\t|\s]+)?([0-9a-z-A-Z_]+)[\t|\s]+([0-9a-z-A-Z_]+)[\t|\s]*=[\t|\s]*([0-9;]+)(.*)',
            _line
        )
        # 匹配到了，是 message 中的一个属性
        if _reg:
            if _reg.group(1) is None:
                _line = f"    optional {_reg.group(2)} {_reg.group(3)} = {_reg.group(4)}{_reg.group(5)}"
        # 记录行
        _newLines.append(_line)
    return listUtils.joinToStr(_newLines, "\n")
