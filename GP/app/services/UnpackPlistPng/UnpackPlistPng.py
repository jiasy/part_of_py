#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import imageUtils
import os, sys

from utils import folderUtils
from utils import fileUtils
from utils import printUtils


class UnpackPlistPng(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(UnpackPlistPng, self).create()

    def destroy(self):
        super(UnpackPlistPng, self).destroy()

    # plist和png所在的文件夹，保持文件夹结构，拆分到指定命名空间内。
    def plistFolderToPngFolder(self, plistFolder_, nameSpace_):
        # 确保源零存在
        if not os.path.exists(plistFolder_):
            printUtils.pError(f"{plistFolder_} not exist")
            sys.exit(1)
        # 指定命名空间存在
        _targetPngRoot = os.path.join(self.resPath, nameSpace_)
        folderUtils.makeSureDirIsExists(_targetPngRoot)
        # 列出所有文件夹
        _folderList = folderUtils.getFolderList(plistFolder_)
        # 遍历所有文件夹
        for _idx in range(len(_folderList)):
            _folderPath = _folderList[_idx]
            _fileList = folderUtils.getFileListInFolder(_folderPath)
            for _idxLoop in range(len(_fileList)):
                _plistPath = _fileList[_idxLoop]  # 找成对的 plist 和 png 文件
                if fileUtils.getSuffix(_plistPath) == ".plist":
                    _belongToSubFolder = os.path.split(_plistPath)[0]
                    _justName = fileUtils.justName(_plistPath)
                    _pngPath = f"{os.path.join(_belongToSubFolder, _justName)}.png"
                    if os.path.exists(_pngPath):
                        # 在命名空间内创建相应的路径
                        _targetPngFolder = os.path.join(_targetPngRoot, str(_belongToSubFolder).split(plistFolder_)[1], _justName)
                        folderUtils.makeSureDirIsExists(_targetPngFolder)
                        imageUtils.gen_png_from_plist(_plistPath, _pngPath, _targetPngFolder)


if __name__ == '__main__':
    _svr_UnpackPlistPng: UnpackPlistPng = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_UnpackPlistPng.resPath))
    pyServiceUtils.printSvrCode(__file__)
