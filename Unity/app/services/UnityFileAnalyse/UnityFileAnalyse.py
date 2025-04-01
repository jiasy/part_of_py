#!/usr/bin/env python3
import sys

from base.supports.Service.BaseService import BaseService
from utils import folderUtils
from utils import pyServiceUtils
import os


# 分析 Prefab 文件
class UnityFileAnalyse(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(UnityFileAnalyse, self).create()

    def destroy(self):
        super(UnityFileAnalyse, self).destroy()

    # 获取并打印工程内指定文件夹内的spine信息
    def getSpineInfosThenPrint(self, projectFolderPath_: str, relativeFolderPath_: str):
        _spineNameToResListDict = self.getSpineInfos(projectFolderPath_, relativeFolderPath_)
        self.printSpineInfo(_spineNameToResListDict)

    #
    def getSpineInfos(self, projectFolderPath_: str, relativeFolderPath_: str):
        # 获取工程中的Spine信息，也就是 Spine 列表
        _targetFolderPath = os.path.join(projectFolderPath_, relativeFolderPath_)
        if not os.path.exists(_targetFolderPath):
            print(f"ERROR : {_targetFolderPath} not exist.")
            sys.exit(1)
        _skeletonDataFilePathList = folderUtils.getFilterFilesInPathReg(_targetFolderPath, [".*SkeletonData\.asset$"])
        _spineNameToResListDict = {}
        for _idx in range(len(_skeletonDataFilePathList)):
            _skeletonDataFilePath = _skeletonDataFilePathList[_idx]
            _skeletonDataFileName = os.path.basename(_skeletonDataFilePath)
            _skeletonDataFileName = _skeletonDataFileName.split("SkeletonData")[0][:-1]  # Spine 名称
            _spineResList = []
            _spineNameToResListDict[_skeletonDataFileName] = _spineResList  # 对应资源列表
            # 所在目录中查找，和自己一样的名称前缀的资源
            _skeletonDataFileLocateFolder = os.path.dirname(_skeletonDataFilePath)
            _spineResFilePathList = folderUtils.getFilterFilesInPathReg(_skeletonDataFileLocateFolder, ["^" + _skeletonDataFileName + ".*"])
            for _idxLoop in range(len(_spineResFilePathList)):
                _spineResFilePath = _spineResFilePathList[_idxLoop]
                if not _spineResFilePath.endswith(".meta"):
                    _relativeSpineFilePath = _spineResFilePath.split(projectFolderPath_)[1]
                    _spineResList.append(_relativeSpineFilePath)
        return _spineNameToResListDict

    #
    def printSpineInfo(self, spineNameToResListDict_: dict):
        for _key in spineNameToResListDict_:
            print(f"{_key} : ")
            _spineList: list = spineNameToResListDict_[_key]
            for _i in range(len(_spineList)):
                _spine = _spineList[_i]
                print(f'    {os.path.basename(_spine)}')
                print(f'        {_spine}')


if __name__ == '__main__':
    _svr: UnityFileAnalyse = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))

    _projectPath = "/disk/XS/wp_client/"
    _relativePath = "Assets/GameResources"
    _svr.getSpineInfosThenPrint(_projectPath, _relativePath)
