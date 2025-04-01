#!/usr/bin/env python3
# Created by nobody at 2023/7/20
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from FGUI.FGUIProject import FGUIProject
from FGUI.FGUIComponent import FGUIComponent
from FGUI.fguiUtils import fguiUtils


class ComponentReferFix(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.assetFolder = None
        self.moduleName = None
        self.commonPackageList = None
        self.fguiProject = None
        self.fguiPackage = None
        self.commonPackageIdDict = None

    def create(self):
        super(ComponentReferFix, self).create()

    def destroy(self):
        super(ComponentReferFix, self).destroy()

    def useCommon(self, _curImgDict: dict):
        _pckId, _commonImgDict = self.fguiProject.getImageFromCommon()
        return _curImgDict

    # 模块中是否有其他模块的引用
    def alertComponentRefer(self):
        for _commonName in self.fguiPackage.componentDict:
            _fguiCmp = FGUIComponent(self.fguiPackage, _commonName)  # 拿组件
            _componentList = _fguiCmp.get_dis_component_list()
            for _idx in range(len(_componentList)):  # 每一个组件
                _componentDict = _componentList[_idx]
                # 删


if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils
    import os

    _subSvr.assetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")
    _subSvr.moduleName = "HeroesHall"
    _subSvr.commonPackageList = [
        "public_icon",
        "public_comp",
        "public_avatar",
        "UiElements",
    ]
    # 工程
    _subSvr.fguiProject = FGUIProject(_subSvr.assetFolder, _subSvr.commonPackageList)
    # 指定模块
    _subSvr.fguiPackage = _subSvr.fguiProject.pkgDict[_subSvr.moduleName]
    # 公用包ID
    _subSvr.commonPackageIdDict = {}
    for _key in _subSvr.fguiProject.commonPkgDict:
        _commonPkgId = _subSvr.fguiProject.commonPkgDict[_key].xmlDict["packageDescription"]["@id"]
        _subSvr.commonPackageIdDict[_commonPkgId] = _key
    # 校验
    _subSvr.alertComponentRefer()
