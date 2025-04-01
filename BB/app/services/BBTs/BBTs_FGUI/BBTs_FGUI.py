#!/usr/bin/env python3
# Created by BB at 2023/8/7
import os.path
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import fileUtils
from utils import folderUtils
from utils import cmdUtils
from FGUI.FGUIPackage import FGUIPackage


class BBTs_FGUI(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(BBTs_FGUI, self).create()

    def destroy(self):
        super(BBTs_FGUI, self).destroy()

    # 通过包名和组件名获取
    def getPath(self, fguiAssetPath_: str, bindDataFolder_: str, pkgName_: str, cmpName_: str):
        _fguiPkg = FGUIPackage(fguiAssetPath_, pkgName_)
        _cmpDict = _fguiPkg.componentDict[cmpName_]
        if _cmpDict == None:
            print(f"ERROR : {pkgName_} - {cmpName_} 不存在")
            sys.exit(1)
        _pkgId, _cmpId = self.getPkgCmpId(fguiAssetPath_, pkgName_, cmpName_)
        _bindDataPath = self.getPathById(bindDataFolder_, _pkgId, _cmpId)
        if not os.path.exists(_bindDataPath):
            print(f"ERROR : {_bindDataPath} 不存在")
            sys.exit(1)
        return _bindDataPath

    def getPkgCmpId(self, fguiAssetPath_: str, pkgName_: str, cmpName_: str):
        _fguiPkg = FGUIPackage(fguiAssetPath_, pkgName_)
        _cmpDict = _fguiPkg.componentDict[cmpName_]
        if _cmpDict is None:
            print(f"ERROR : {pkgName_} - {cmpName_} 不存在")
            sys.exit(1)
        return _fguiPkg.id, _cmpDict["@id"]

    # 通过 Id 获取
    def getPathById(self, bindDataFolder_, pkgId_: str, cmpId_: str):
        _bindDataPath = os.path.join(bindDataFolder_, f'{pkgId_}{cmpId_}.bindData')
        return _bindDataPath

    # 通过 package 和 component 的名称来查找 bindData 路径。
    def findAndOpenBindData(self, fguiAssetPath_: str, bindDataFolder_: str, pkgName_: str, cmpName_: str):
        _bindDataPath = self.getPath(fguiAssetPath_, bindDataFolder_, pkgName_, cmpName_)
        cmdUtils.openWithSublime(_bindDataPath)
        print(f"bindData 路径为 : {_bindDataPath}")

    def findAndDeleteBindData(self, fguiAssetPath_: str, bindDataFolder_: str, pkgName_: str, cmpName_: str):
        _bindDataPath = self.getPath(fguiAssetPath_, bindDataFolder_, pkgName_, cmpName_)
        fileUtils.removeExistFile(_bindDataPath)
        print(f"bindData 删除 : {_bindDataPath}")

    # 导出资源放置到新工程，其id值会发生变化，导致 bindData 丢失。这里将bindData 找回并放置到新工程中。
    # 旧工程中有组件，在新工程的对应 pkg 目录中查找，找到的话，就将旧的 bindData 拷贝过去
    def vmAndBindDatasCopy(self, oldFguiAssetPath_: str, oldBindDataFolder_: str, oldVMFolder_: str, newFguiAssPath_: str, newBindDataFolder_: str, newVMFolder_: str, newVMCodeFolder_: str, pkgName_: str):
        # 删

    def getBindDataByPkgName(self, fguiAssetPath_: str, oldPkgName_: str, newPkgName_: str, bindDataFolder_: str):
        # 删


if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    from utils.CompanyUtil import Company_BB_Utils

    _fguiAssetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")
    _bindDataFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/bindData")
    # 查找并用 Sublime 打开
    # _subSvr.findAndOpenBindData(_fguiAssetFolder, _bindDataFolder, "HeroBag", "HeroInfoStatsLayer")
    # 删除
    # _subSvr.findAndDeleteBindData(_fguiAssetFolder, _bindDataFolder, "HeroBag", "HeroEvelotionSkill")
    # _subSvr.findAndDeleteBindData(_fguiAssetFolder, _bindDataFolder, "HeroBag", "HeroEvolutionItem")
    # _subSvr.findAndDeleteBindData(_fguiAssetFolder, _bindDataFolder, "HeroBag", "HeroEvolutionLayer")

    _subSvr.getBindDataByPkgName(_fguiAssetFolder, "HeroBag", "HeroBag_01", _bindDataFolder)

    sys.exit(1)

    # 新的
    _new_fguiAssetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")
    _new_bindDataFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/bindData")
    _new_vmFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/vmJson")
    _new_vmCodeFolder = os.path.join(Company_BB_Utils.getSLGRoot(), "FGUI_Sample/project_ts_slgjp/src/Game/Module/Science/VM")
    # 旧的
    _old_fguiAssetFolder = os.path.join(Company_BB_Utils.getSLGRoot(), "FGUI_Sample/SLG_FGUI/FGUIProject/assets")
    _old_bindDataFolder = os.path.join(Company_BB_Utils.getSLGRoot(), "FGUI_Sample/SLG_FGUI/FGUIProject/bindData")
    _old_vmFolder = os.path.join(Company_BB_Utils.getSLGRoot(), "FGUI_Sample/SLG_FGUI/FGUIProject/vmjson")

    _subSvr.vmAndBindDatasCopy(_old_fguiAssetFolder, _old_bindDataFolder, _old_vmFolder, _new_fguiAssetFolder, _new_bindDataFolder, _new_vmFolder, _new_vmCodeFolder, "Tech")
