#!/usr/bin/env python3
# Created by nobody at 2023/7/18
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FGUI.app.services.PackageFix import PackageFix


class ListFix(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(ListFix, self).create()

    def destroy(self):
        super(ListFix, self).destroy()

    def checkListInfo(self, xmlPath_: str, listInfo_: dict):
        _belongToService: PackageFix = self.belongToService
        if "@autoClearItems" not in listInfo_ or listInfo_["@autoClearItems"] is False:
            print(f'ERROR : {xmlPath_.split(_belongToService.fguiAssetFolder)[1]} 有 List 忘记打开 发布时自动清空')

    def checkList(self, xmlPath_: str, xmlContentDict_: dict):
        if "list" in xmlContentDict_["component"]["displayList"]:
            _listInfoList = xmlContentDict_["component"]["displayList"]["list"]
            if _listInfoList is list:
                for _idxLoop in range(len(_listInfoList)):
                    self.checkListInfo(xmlPath_, _listInfoList[_idxLoop])
            else:
                self.checkListInfo(xmlPath_, _listInfoList)


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
