# !/usr/bin/env python3
import os.path
import sys

from FGUI.FGUIProject import FGUIProject
from FGUI.app.services.CreateUICode.Fgui_Dis_BB.Fgui_UI_BB import Fgui_UI_BB
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import dictUtils
from utils import printUtils
from utils import fileUtils

if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)

    from utils.CompanyUtil import Company_BB_Utils
    import os

    _tsCodeFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/src")
    _tsUIFolder = os.path.join(_tsCodeFolder, "Game/Module")

    _fguiAssetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets/")
    _fguiProject = FGUIProject(_fguiAssetFolder, [])

    # FGUI 解析目标相关配置
    _pkgName = "Hero"
    _cmpName = "HeroInfoUpgrade_01_Layer"
    _fguiCmp = _fguiProject.getComponentByName(_pkgName, _cmpName)  # FGUI 组件

    # # 打印组件内容
    # printUtils.printDictStruct("_fguiCmp", _fguiCmp.xmlContentDict)
    # dictUtils.printAsKeyValue("_fguiCmp", _fguiCmp.xmlContentDict["component"])
    # sys.exit(1)

    # 代码生成相关配置
    _codeModuleName = "HeroBag"
    _viewName = "HeroInfoUpgrade"
    _tsCodeFolderPath = os.path.join(_tsUIFolder, _codeModuleName, "View")
    _tsPlaceCodePath = os.path.join(_tsCodeFolderPath, f"View{_viewName}Place.ts")  # 摆放，直接覆盖
    _tsLogicCodePath = os.path.join(_tsCodeFolderPath, f"View{_viewName}Logic.ts")  # 逻辑，只生成一次。以免覆盖掉手写内容

    # 解析 FGUI 生成 代码
    _uiObj = Fgui_UI_BB(_fguiCmp)
    fileUtils.writeFileWithStr(_tsPlaceCodePath, _uiObj.getPlaceCode(_viewName))
    if not os.path.exists(_tsLogicCodePath):
        fileUtils.writeFileWithStr(_tsLogicCodePath, _uiObj.getLogicCode(_viewName))
