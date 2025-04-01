#!/usr/bin/env python3
# Created by BB at 2023/10/19

from utils import pyServiceUtils
from utils import excelDataUtils
from base.supports.Base.BaseInService import BaseInService
import os
from utils.CompanyUtil import Company_BB_Utils


class BBTs_Config(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(BBTs_Config, self).create()

    def destroy(self):
        super(BBTs_Config, self).destroy()

    def createData(self, excelFolderPath_: str, excelName_: str):
        _excelFile = os.path.join(excelFolderPath_, f'{excelName_}.xlsm')
        _dataSheetDict, _fieldDataColDictDict = excelDataUtils.getCacheExcelData(self.subResPath, _excelFile)
        return _dataSheetDict


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    _excelFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
