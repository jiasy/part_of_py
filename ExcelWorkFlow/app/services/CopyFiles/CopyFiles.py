#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import folderUtils
import shutil
import os


# 拷贝文件
class CopyFiles(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(CopyFiles, self).create()

    # 拷贝，只拷贝并替换已经存在的文件
    def coverFiles(self, typeFilters_: list, sourceFolderPath_: str, targetFolderPath_: str):
        print("CopyFiles -> coverFiles : \n    " + sourceFolderPath_ + " -> " + targetFolderPath_)
        _filePathDict = folderUtils.getFilePathKeyValue(targetFolderPath_, typeFilters_)
        for _fileName, _filePath in _filePathDict.items():
            _shortPath = _filePath.split(targetFolderPath_)[1]
            _tarfilePath = targetFolderPath_ + _shortPath
            _sourcefilePath = sourceFolderPath_ + _shortPath
            # 存在这文件，就拷贝
            if os.path.exists(_sourcefilePath):
                print('        copy : ' + str(_fileName))
                shutil.copy(_sourcefilePath, _tarfilePath)
            else:
                print('x-      pass : ' + str(_fileName) + " not exist.")

    def destroy(self):
        super(CopyFiles, self).destroy()
