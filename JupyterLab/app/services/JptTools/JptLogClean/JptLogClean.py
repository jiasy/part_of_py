#!/usr/bin/env python3
# Created by nobody at 2023/12/9
import os.path

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import cmdUtils
from utils import folderUtils


class JptLogClean(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(JptLogClean, self).create()

    def destroy(self):
        super(JptLogClean, self).destroy()

    # 清理 文件内的日志
    def cleanPynbLogInFolder(self, pynbFolder_: str):
        _pynbFileList = folderUtils.getFileListInFolder(pynbFolder_, [".ipynb"])
        for _i in range(len(_pynbFileList)):
            self.cleanPynbLog(_pynbFileList[_i])

    def cleanPynbLog(self, pynbFilePath_: str):
        _cmd = "jupyter nbconvert"
        _cmd = f"{_cmd} --ClearOutputPreprocessor.enabled=True"
        _cmd = f"{_cmd} --inplace {pynbFilePath_}"
        cmdUtils.doStrAsCmd(_cmd, os.path.split(pynbFilePath_)[0])


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr: JptLogClean = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    _subSvr.cleanPynbLogInFolder("/Users/nobody/Documents/develop/GitHub/Services/PY_Service/JupyterLab/")
