#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import fileUtils
from utils import folderUtils
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from FGUI.app.services.PackageFix.FontFix import FontFix
from FGUI.app.services.PackageFix.ListFix import ListFix
from FGUI.app.services.PackageFix.ImageFix import ImageFix
from FGUI.FGUIPackage import FGUIPackage


class PackageFix(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        self._assetFolder = None
        self.fontFix: FontFix = self.getSubClassObject("FontFix")  # 字体修复
        self.listFix: ListFix = self.getSubClassObject("ListFix")  # 列表修复
        self.imageFix: ImageFix = self.getSubClassObject("ImageFix")  # 图片修复

    @property
    def assetFolder(self):
        return self._assetFolder

    @assetFolder.setter
    def assetFolder(self, value_: str):
        self._assetFolder = value_

    def create(self):
        super(PackageFix, self).create()

    def destroy(self):
        super(PackageFix, self).destroy()

    def checkPackage(self, folderName_):
        _fguiPackage = FGUIPackage(self.assetFolder, folderName_)
        if _fguiPackage.isNew:
            print(f'{folderName_} 不存在 package')
            return
        else:
            print(f'检查中 {folderName_}')
        # 组件信息
        _componentAndPackagePathList = folderUtils.getFilterFilesInPath(os.path.join(self.assetFolder, folderName_), [".xml"])
        for _idx in range(len(_componentAndPackagePathList)):
            _componentAndPackagePath = _componentAndPackagePathList[_idx]
            if fileUtils.justName(_componentAndPackagePath) == "package":
                continue  # package.xml 不是 组件，跳过
            _xmlContent = fileUtils.readFromFile(_componentAndPackagePath)
            _xmlContentDict = bf.data(fromstring(_xmlContent))
            if "displayList" in _xmlContentDict["component"]:
                self.listFix.checkList(_componentAndPackagePath, _xmlContentDict)  # 检查列表
                self.imageFix.fixLostImageInPackage(_componentAndPackagePath, _xmlContentDict, _fguiPackage.xmlDict)  # 修复图片使用的路径

    def checkAllPackage(self):
        _folderPathList = folderUtils.getFolderNameListJustOneDepth(self.assetFolder)
        for _i in range(len(_folderPathList)):
            self.checkPackage(_folderPathList[_i])


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils
    import os
    #
    # _svr.assetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")
    # _svr.checkPackage("Castle")
