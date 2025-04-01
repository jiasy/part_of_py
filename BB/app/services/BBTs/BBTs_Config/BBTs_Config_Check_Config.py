import sys

from BB.app.services.BBTs.BBTs_Config.ConfigLogicRoot import ConfigLogicRoot
from BB.app.services.BBTs.BBTs_Config.BBTs_Config import BBTs_Config
from BB.app.services.BBTs.BBTs_Config.ConfgClass.GameCondition.GameCondition_Sheet import GameCondition_Sheet
from BB.app.services.BBTs.BBTs_Config.ConfgClass.Hero.Hero_Sheet import Hero_Sheet
from BB.app.services.BBTs.BBTs_Config.ConfgClass.Hero.HeroStar_Sheet import HeroStar_Sheet
from BB.app.services.BBTs.BBTs_Config.ConfgClass.Hero.HeroLevel_Sheet import HeroLevel_Sheet
from BB.app.services.BBTs.BBTs_Config.ConfgClass.GameModifier.GameModifier_Sheet import GameModifier_Sheet
from utils import pyServiceUtils
from utils.infoUtils.InfoColor import InfoColor
from utils.infoUtils.InfoType import InfoType

from typing import Union
from utils.CompanyUtil import Company_BB_Utils
import os

_excelFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
_fguiAssetFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets/")
# _assetListTxtPath = os.path.join(Company_BB_Utils.getSLGProjectPath(),"asset_bundle/all/iOs/processed_bundles/AssetList.txt")
_assetListTxtPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "asset_bundle/all/Android/processed_bundles/AssetList.txt")
_artFolderPath = os.path.join(Company_BB_Utils.getSLGRoot(), "DEV/projects/art/dev/project_art/dev/Assets/")
_picFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/demo/sc/pic/")


def printLocalStr(cfgLogicRoot_: ConfigLogicRoot, name_: str):
    cfgLogicRoot_.info.newLine().addInfo(name_, InfoColor.Black, InfoColor.Yellow).addBlank().addInfo(f' {cfgLogicRoot_.getLocalStr(name_)} ', InfoColor.Yellow)
    cfgLogicRoot_.info.doPrint(InfoType.Color)


def printLocalNameByCHN(cfgLogicRoot_: ConfigLogicRoot, chnStr_: str):
    cfgLogicRoot_.info.newLine().addInfo(chnStr_, InfoColor.Black, InfoColor.Yellow).addBlank().addInfo(f' {cfgLogicRoot_.getLocalizationCfgByCHN(chnStr_).Name} ', InfoColor.Yellow)
    cfgLogicRoot_.info.doPrint(InfoType.Color)


# 检查科技表中的 GameCondition 字段
def checkScienceGameCondition(cfgLogicRoot_: ConfigLogicRoot):
    # GameCondition 字段的内容是从 GameCondition 表中获取，判断这些值是否都配置过了
    _needExcel = "SwiftScience"  # 从那个表的那个字段起始
    _needSheet = "ScienceConfig"
    _needKey = "GameCondition"
    _targetExcel = "GameCondition"  # 向那个表的那个字段所要值
    _targetSheet = "GameCondition"
    _targetKey = "Id"
    cfgLogicRoot_.checkConfigRelation(_needExcel, _needSheet, _needKey, _targetExcel, _targetSheet, _targetKey)


# 格式化
def formatByType(type_: int, value_: int):
    if type_ == 1:
        return f'{value_}'
    elif type_ == 5:
        return f'{float(format(value_ / 100, ".2f")) * 100 / 100}%'
    else:
        print(f"ERROR : 未实现 {type_}")
        sys.exit(1)


# 英雄 heroId_ ，在 level_ 等级下，在 star_ 星级下 的属性
def checkHero(cfgLogicRoot_: ConfigLogicRoot, heroId_: int, level_: int, star_: int):
    # 英雄配置
    _heroCfgs: list[Hero_Sheet] = cfgLogicRoot_.getCfgList("Hero", "Hero")
    for _i in range(len(_heroCfgs)):
        _hero = _heroCfgs[_i]
        if _hero.Id == heroId_:
            # 值配置
            _gameModifierCfg1: GameModifier_Sheet = cfgLogicRoot_.getMatchValueCfgList("GameModifier", "GameModifier", "Id", _hero.RtsGameModifier[0][0])[0]
            _gameModifierCfg2: GameModifier_Sheet = cfgLogicRoot_.getMatchValueCfgList("GameModifier", "GameModifier", "Id", _hero.RtsGameModifier[1][0])[0]
            _gameModifierCfg3: GameModifier_Sheet = cfgLogicRoot_.getMatchValueCfgList("GameModifier", "GameModifier", "Id", _hero.RtsGameModifier[2][0])[0]
            _gameModifierCfg4: GameModifier_Sheet = cfgLogicRoot_.getMatchValueCfgList("GameModifier", "GameModifier", "Id", _hero.SlgTroopGameModifier[0][0])[0]
            _gameModifierCfg5: GameModifier_Sheet = cfgLogicRoot_.getMatchValueCfgList("GameModifier", "GameModifier", "Id", _hero.SlgTroopGameModifier[1][0])[0]
            # 值名称
            _valueName1 = cfgLogicRoot_.getLocalStr(_gameModifierCfg1.Name)
            _valueName2 = cfgLogicRoot_.getLocalStr(_gameModifierCfg2.Name)
            _valueName3 = cfgLogicRoot_.getLocalStr(_gameModifierCfg3.Name)
            _valueName4 = cfgLogicRoot_.getLocalStr(_gameModifierCfg4.Name)
            _valueName5 = cfgLogicRoot_.getLocalStr(_gameModifierCfg5.Name)
            # 基础值
            _baseValue1 = _hero.RtsGameModifier[0][1]
            _baseValue2 = _hero.RtsGameModifier[1][1]
            _baseValue3 = _hero.RtsGameModifier[2][1]
            _baseValue4 = _hero.SlgTroopGameModifier[0][1]
            _baseValue5 = _hero.SlgTroopGameModifier[1][1]
            # 打印基础值
            cfgLogicRoot_.info.newLine().addInfo(f' {heroId_} ----------------------------------------------------------', InfoColor.Black, InfoColor.Blue)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addInfo(" 基础值 --------------------------------------", InfoColor.Black, InfoColor.Yellow)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName1} : {formatByType(_gameModifierCfg1.GameNumberType, _baseValue1)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_baseValue1}]", InfoColor.Red, InfoColor.Black)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName2} : {formatByType(_gameModifierCfg2.GameNumberType, _baseValue2)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_baseValue2}]", InfoColor.Red, InfoColor.Black)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName3} : {formatByType(_gameModifierCfg3.GameNumberType, _baseValue3)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_baseValue3}]", InfoColor.Red, InfoColor.Black)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName4} : {formatByType(_gameModifierCfg4.GameNumberType, _baseValue4)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_baseValue4}]", InfoColor.Red, InfoColor.Black)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName5} : {formatByType(_gameModifierCfg5.GameNumberType, _baseValue5)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_baseValue5}]", InfoColor.Red, InfoColor.Black)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addInfo(f" 加成后 {level_}级 - {star_}阶 --------------------------------------", InfoColor.Black, InfoColor.Yellow)
            # 指定 Plan 下的 level 配置
            _levelCfg = cfgLogicRoot_.getDoubleMatchValueCfgList("Hero", "HeroLevel", "HeroLevelPlan", _hero.HeroLevelPlan, "Level", level_)[0]
            _starCfig = cfgLogicRoot_.getDoubleMatchValueCfgList("Hero", "HeroStar", "HeroStarPlan", _hero.HeroStarPlan, "Level", star_)[0]
            # 计算当前的值
            _currentValue1 = _baseValue1 * (_levelCfg.RtsGameModifierFactor + _starCfig.RtsGameModifierFactor) / 10000
            _currentValue2 = _baseValue2 * (_levelCfg.RtsGameModifierFactor + _starCfig.RtsGameModifierFactor) / 10000
            _currentValue3 = _baseValue3 * (_levelCfg.RtsGameModifierFactor + _starCfig.RtsGameModifierFactor) / 10000
            _currentValue4 = _baseValue4 * (_levelCfg.SlgGameModifierFactor + _starCfig.SlgGameModifierFactor) / 10000
            _currentValue5 = _baseValue5 * (_levelCfg.SlgGameModifierFactor + _starCfig.SlgGameModifierFactor) / 10000
            # 显示当前值
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName1} : {formatByType(_gameModifierCfg1.GameNumberType, _currentValue1)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_currentValue1}]", InfoColor.Red, InfoColor.Black)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName2} : {formatByType(_gameModifierCfg2.GameNumberType, _currentValue2)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_currentValue2}]", InfoColor.Red, InfoColor.Black)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName3} : {formatByType(_gameModifierCfg3.GameNumberType, _currentValue3)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_currentValue3}]", InfoColor.Red, InfoColor.Black)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName4} : {formatByType(_gameModifierCfg4.GameNumberType, _currentValue4)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_currentValue4}]", InfoColor.Red, InfoColor.Black)
            cfgLogicRoot_.info.newLine().addBlank(InfoColor.Blue).addBlank(InfoColor.Yellow).addInfo(f" {_valueName5} : {formatByType(_gameModifierCfg5.GameNumberType, _currentValue5)} ", InfoColor.Black, InfoColor.Red).addInfo(f"[{_currentValue5}]", InfoColor.Red, InfoColor.Black)
            # 打印
            cfgLogicRoot_.info.doPrint(InfoType.Color)
            break


if __name__ == '__main__':
    _subSvr: BBTs_Config = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    _excelName = "GameGuide"  # 随意用一个，要的是基类的各种生成方法
    _cfgLogicRoot = ConfigLogicRoot(_subSvr, _excelFolderPath, _excelName)

    # 打印翻译
    printLocalStr(_cfgLogicRoot, "newtec_tips_04")
    sys.exit(1)
    printLocalNameByCHN(_cfgLogicRoot, "请求帮助成功")

    # 检查科技表中的 GameCondition 字段配置
    checkScienceGameCondition(_cfgLogicRoot)

    # 打印指定英雄的信息
    checkHero(_cfgLogicRoot, 10515, 1, 0)
