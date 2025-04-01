import sys
from colorama import init
from BB.app.services.BBTs.BBTs_Config.Check_GameGuide.GameGuideRoot import GameGuideRoot
from BB.app.services.BBTs.BBTs_Config.BBTs_Config import BBTs_Config
from BB.app.services.BBTs.BBTs_Config.ConfigExcelRoot import ConfigExcelRoot
from BB.app.services.BBTs.BBTs_Config.ConfigSheet import ConfigSheet
from utils import pyServiceUtils
from utils import fileUtils
from utils import excelDataUtils
import re
import os

from utils.CompanyUtil import Company_BB_Utils

_excelFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
_fguiAssetFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets/")
_tsFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/src")


# 获取当前使用的 ui
def getUseLayerPathDict():
    # 当前记录过的界面
    _tsPath = os.path.join(_tsFolderPath, "Game/Common/IDTypeEnum.ts")
    _lines = fileUtils.linesFromFile(_tsPath)
    _backUiPathDict = {}
    for _cId in range(len(_lines)):
        _line = _lines[_cId]
        _funcReg = re.search(r'^\s*([a-zA-Z0-9_]+)\s*=\s*\"([a-zA-Z0-9_]+)/([a-zA-Z0-9_]+)\"', _line)
        if _funcReg:
            _backUiPathDict[_funcReg.group(1)] = f"{_funcReg.group(2)}/{_funcReg.group(3)}"
    return _backUiPathDict


def getSheetCfg(_configExcelRoot: ConfigExcelRoot, sheetName_: str, id_: int, SheetClass: ConfigSheet):
    sheetCfgList = _configExcelRoot.getSheetDataList(sheetName_, SheetClass)
    sheetCfg: SheetClass = None
    for _i in range(len(sheetCfgList)):
        gameGuideStepCfg: SheetClass = sheetCfgList[_i]
        if gameGuideStepCfg.Id == id_:
            sheetCfg = gameGuideStepCfg
            break
    if sheetCfg is None:
        print(f"ERROR : {sheetName_} - {id_} not found")
        sys.exit(1)
    return sheetCfg


# 打开指定的 step 的 Excel 并将其标记
def openExcelMarkStep(bbtsConfig_: BBTs_Config, fguiAssetFolderPath_: str, excelFolderPath_: str, excelName_: str, stepId_: int):
    _dataSheetDict = bbtsConfig_.createData(excelFolderPath_, excelName_)  # 配置数据
    _guideRoot = GameGuideRoot(_dataSheetDict, bbtsConfig_, excelFolderPath_, excelName_, fguiAssetFolderPath_, [], _tsFolderPath)  # 数据关系获取
    _group = _guideRoot.getGroupByStepId(stepId_)
    _guide = _guideRoot.getGuideByGroupId(_group.Id)
    _guideRoot.markGameGuideById(_guide.Id, True)  # 标记 Guide
    _guideRoot.markGameGuideGroupById(_group.Id, True)  # 标记 Group
    _guideRoot.markGameGuideStepById(stepId_, True)  # 最后 标记 Step


if __name__ == '__main__':
    from utils.infoUtils.InfoType import InfoType

    _subSvr: BBTs_Config = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    _excelName = "GameGuide"

    # 配置数据
    _dataSheetDict = _subSvr.createData(_excelFolderPath, _excelName)
    # 数据关系获取
    _guideRoot = GameGuideRoot(_dataSheetDict, _subSvr, _excelFolderPath, _excelName, _fguiAssetFolderPath, getUseLayerPathDict(), _tsFolderPath)
    # _guideRoot.dumpRelation()  # 打印其关系
    _guideRoot.check()  # 校验
    # 初始化 colorama
    init(autoreset=True)
    _guideRoot.doDesc()  # 进行描述
    # _guideRoot.doPrint(InfoType.Color)  # 进行打印
    _guideRoot.doPrint(InfoType.ExcelCell, "/Users/XS/Downloads/rar/PythonExcel/Guide_Desc.xlsx")  # 进行 Excel 排版存留
    # _guideRoot.doPrint(InfoType.ExcelShape, "/Users/XS/Downloads/rar/PythonExcel/Guide_Desc.xlsx")  # 进行 Excel 排版存留
