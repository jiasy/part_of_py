#!/usr/bin/env python3
# Created by nobody at 2023/7/20
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from FGUI.FGUIProject import FGUIProject
from FGUI.FGUIComponent import FGUIComponent
from FGUI.fguiUtils import fguiReplaceUtils
from FGUI.fguiUtils import fguiUtils


class CommonImageFix(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.assetFolder = None
        self.moduleName = None
        self.commonPackageList = None
        self.fguiProject = None
        self.fguiPackage = None

    def create(self):
        super(CommonImageFix, self).create()

    def destroy(self):
        super(CommonImageFix, self).destroy()

    def useCommon(self, _curImgDict: dict):
        _pckId, _commonImgDict = self.fguiProject.getImageFromCommon()

        return _curImgDict

    def fixPicPathToCommon(self, moduleName_: str, cmpName_: str = None):
        if self.fguiProject is None:
            self.fguiProject = FGUIProject(self.assetFolder, self.commonPackageList)
        self.fguiPackage = self.fguiProject.pkgDict[moduleName_]
        for _commonName in self.fguiPackage.componentDict:
            if cmpName_ is not None and cmpName_ != _commonName:
                continue  # 指定某个组件的时候
            _fguiCmp = FGUIComponent(self.fguiPackage, _commonName)  # 从 Component 换掉
            _imageList = _fguiCmp.get_dis_image_list()
            for _i in range(len(_imageList)):
                _imgDict = _imageList[_i]
                _picName = _imgDict["@fileName"].split("/")[-1].split(".png")[0]
                _pckId, _commonImgDict = self.fguiProject.getImageFromCommon(_picName)
                if _commonImgDict is not None:  # 有公共组件
                    if "@pkg" not in _imgDict or _imgDict["@pkg"] != _pckId:  # 没引用其他包，或引用的不是公共包
                        # 删


# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr: CommonImageFix = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils
    import os

    _subSvr.assetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")
    _subSvr.moduleName = "HeroBag"
    # 指定公共图片的包，顺序决定取图先后
    _subSvr.commonPackageList = [
        "public_icon",
        "public_comp",
        "public_avatar",
        "UiElements",
    ]
    # 将指定的包中所有图片更换成公共包中的同名图片
    _subSvr.fixPicPathToCommon("LordInfo")
