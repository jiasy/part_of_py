#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, shutil

CUR_DIR = os.path.abspath('.')


def getFilterFilesInPath(folderPath_: str, filters_: list):
    _allFilePaths = []
    for root, dirs, files in os.walk(folderPath_):
        if filters_:
            _realFilePaths = [os.path.join(root, _file) for _file in files if
                              os.path.splitext(_file)[1] in filters_]
        else:
            _realFilePaths = [os.path.join(root, _file) for _file in files]
        _allFilePaths = _allFilePaths + _realFilePaths
    return _allFilePaths


def makeSureDirIsExists(path_: str):
    # 路径存在
    if os.path.exists(path_):
        # 不是文件夹，返回False
        if not os.path.isdir(path_):
            print("路径 " + path_ + " 存在，但不是一个文件夹。")
            return False
        else:
            return True
    else:
        os.makedirs(path_)


def copyWithStructure(type_: str):
    sourceFolderPath_ = os.path.join(CUR_DIR, "Assets")
    targetFolderPath_ = os.path.join(CUR_DIR, type_)
    print(type_ + " : " + str(sourceFolderPath_) + ' -> ' + str(targetFolderPath_))
    _filePathList = getFilterFilesInPath(sourceFolderPath_, ["." + type_])
    for _i in range(len(_filePathList)):
        _shortPath = _filePathList[_i].split(sourceFolderPath_)[1]
        _tarfilePath = targetFolderPath_ + _shortPath
        _sourcefilePath = sourceFolderPath_ + _shortPath
        _targetFileLocalFolderPath = os.path.split(_tarfilePath)[0]
        makeSureDirIsExists(_targetFileLocalFolderPath)
        shutil.copy(_sourcefilePath, _tarfilePath)


# 放到 Assets 上层中执行脚本，将指定的某一个类型，按照文件结构拷贝出来，放置在同级的 类型 目录中
if __name__ == '__main__':
    # 指定类型拷出，到指定类型名称文件夹中。
    copyWithStructure("cs")  # 将 Assets 中 .cs 文件拷贝出来，放置到 cs 文件夹中。
