from termcolor import colored
from utils.infoUtils.InfoType import InfoType
from BB.app.services.BBTs.BBTs_Config.ConfigLogicRoot import ConfigLogicRoot
from BB.app.services.BBTs.BBTs_Config.BBTs_Config import BBTs_Config
from BB.app.services.BBTs.BBTs_Config.Check_GameGuide.GameGuide import GameGuide
from BB.app.services.BBTs.BBTs_Config.Check_GameGuide.GameGuideGroup import GameGuideGroup
from BB.app.services.BBTs.BBTs_Config.Check_GameGuide.GameGuideStep import GameGuideStep
from FGUI.FGUIProject import FGUIProject
from utils import pyServiceUtils
from utils import excelDataUtils
import sys
from colorama import init


class GameGuideRoot(ConfigLogicRoot):
    def __init__(self, excelData_, subSvr_BBTs_Config_: BBTs_Config, excelFolderPath_: str, excelName_: str, fguiAssetFolderPath_: str, uiPathDict_: dict, tsFolderPath_: str):
        super().__init__(subSvr_BBTs_Config_, excelFolderPath_, excelName_)
        self.guideList: list[GameGuide] = []  # 所有引导步骤
        self.isRelationCreated = False
        self.excelData = excelData_
        self.fguiProject = FGUIProject(fguiAssetFolderPath_, [])
        self.uiPathDict: dict = uiPathDict_  # 实际使用的UI
        self.tsFolderPath = tsFolderPath_
        self.createRelation()  # 创建关系
        self.mainUIPath = "MainUI_01/MainUILayer_01"

    # 删


if __name__ == '__main__':
    from BB.app.services.BBTs.BBTs_Config import BBTs_Config
    from utils.CompanyUtil import Company_BB_Utils
    import os

    _subSvr: BBTs_Config = pyServiceUtils.getSubSvrByName("BB", "BBTs", "BBTs_Config")

    init(autoreset=True)

    _excelName = "GameGuide"
    # 配置数据

    _excelFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
    _excelFile = os.path.join(_excelFolderPath, f'{_excelName}.xlsm')
    _dataSheetDict, _ = _subSvr.getCacheExcelData(_subSvr.subResPath, _excelFile)
    _fguiAssetFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets/")
    # 数据关系获取
    _guideRoot = GameGuideRoot(_dataSheetDict, _subSvr, _excelFolderPath, _excelName, _fguiAssetFolderPath, [])
    _guideRoot.printGuideGroupStepByStepId(130104)
