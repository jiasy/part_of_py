#!/usr/bin/env python3
# Created by nobody at 2020/11/23

from Excel.ExcelBaseInService import ExcelBaseInService
import os
import re
import sys
from utils import sysUtils
from utils import fileUtils
from utils import regUtils
from utils import fileCopyUtils
from utils import folderUtils
from pathlib import Path
from utils import pyServiceUtils

class AirTest(ExcelBaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.funcDict = {
            "ClearCreateJpg": {  # 清理用来识别图像的截屏文件。
                "createJpgFolder": "用来识别图片的手机截屏存放文件夹",
            },
            "BackupCodesAndPngs": {  # 将代码中使用到的png图片获取到新文件夹。删除或备份png文件，将新文件夹下的文件拷贝回去，就做到了去除无用png。
                "projectFolder": ".air .py .png 所在的工程文件夹",
                "projectName": "测试工程名",
            }
        }

    def create(self):
        super(AirTest, self).create()

    def destroy(self):
        super(AirTest, self).destroy()

    def ClearCreateJpg(self, dParameters_):
        _createJpgFolderPath = sysUtils.folderPathFixEnd(dParameters_["createJpgFolder"])
        _jpgPathList = folderUtils.getFilterFilesInPath(_createJpgFolderPath, [".jpg"])
        for _i in range(len(_jpgPathList)):
            _jpgPath = _jpgPathList[_i]
            _jpgName = os.path.basename(_jpgPath)
            _jpgResult = re.search(r'(\d+).jpg', _jpgName)  # 纯数字名称，满足条件就删除
            if _jpgResult:
                fileUtils.removeExistFile(_jpgPath)

    def BackupCodesAndPngs(self, dParameters_):
        _projectFolderPath = sysUtils.folderPathFixEnd(dParameters_["projectFolder"])
        _projectName = dParameters_["projectName"]
        _airAndPyPathList = folderUtils.getFilterFilesInPath(_projectFolderPath, [".air", ".py"])
        # 匹配 r"tpl1606022416813.png" 这样的内容
        _groupReg = r"r\"(.*)\.png\""
        # 要拷贝的png文件名
        _pngPathList = []
        for _i in range(len(_airAndPyPathList)):
            _airAndPyPath = _airAndPyPathList[_i]
            _matchGroupList = regUtils.getMatchGroupStrList(_airAndPyPath, _groupReg)  # 得到匹配的group阵列
            for _j in range(len(_matchGroupList)):
                _pngNameWithOutSuffix = _matchGroupList[_j][0]
                _pngPath = _projectFolderPath + "/" + _pngNameWithOutSuffix + ".png"
                if not _pngPath in _pngPathList:  # 没有记录过，就记录
                    _pngPathList.append(_pngPath)
        _tempPicsFolderPath = _projectFolderPath + "tempPics/"
        print("    拷贝代码实际使用图片到临时目录 : " + _tempPicsFolderPath)
        fileCopyUtils.copyFilesToFolder(_pngPathList, _tempPicsFolderPath)
        _backupProjectFolderPath = str(Path(self.subResPath + "/" + _projectName))  # 在资源文件内备份
        print('    备份位置 : ' + str(_backupProjectFolderPath))
        folderUtils.makeSureDirIsExists(_backupProjectFolderPath)
        print('    备份代码')
        fileCopyUtils.copyFilesInFolderTo(
            [".py", ".air"],
            _projectFolderPath,
            _backupProjectFolderPath,
            "include"
        )
        print('    备份图片')
        fileCopyUtils.copyFilesInFolderTo(
            [".png"],
            _tempPicsFolderPath,
            _backupProjectFolderPath,
            "include"
        )
        print('    删除临时目录')
        folderUtils.removeTree(_tempPicsFolderPath)


import Main
if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    pyServiceUtils.printSubSvrCode(__file__)

