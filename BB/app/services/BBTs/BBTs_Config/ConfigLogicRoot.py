import sys
import json
from typing import Union

from BB.app.services.BBTs.BBTs_Config.ConfgClass.ConfigSheetBase import ConfigLogicRootBase
from BB.app.services.BBTs.BBTs_Config.ConfigSheet import ConfigSheet
from utils import fileUtils
from utils import folderUtils
from utils import dictUtils
from utils import printUtils
from utils import pyServiceUtils

from BB.app.services.BBTs.BBTs_Config.ConfgClass.Localization.Localization_Sheet import Localization_Sheet
from BB.app.services.BBTs.BBTs_Config.BBTs_Config import BBTs_Config

from utils.infoUtils.InfoRoot import InfoRoot
from utils.infoUtils.InfoColor import InfoColor
from utils.infoUtils.InfoType import InfoType


class ConfigLogicRoot(ConfigLogicRootBase):
    def __init__(self, subSvr_BBTs_Config_: BBTs_Config, excelFolderPath_: str, excelName_: str):
        super().__init__(subSvr_BBTs_Config_, excelFolderPath_)
        self.subResPath = self.subSvr_BBTs_Config.subResPath
        self.excelName = excelName_
        self.info: InfoRoot = InfoRoot()

    # SAMPLE Class 通过字符串获取方法执行或属性比较
    # SAMPLE Union 指定指定参数的类型范围
    def getMatchValueCfgList(self, excelName_: str, sheetName_: str, key_: str, value_: Union[str, int]):
        # 检查 value_ 的类型
        if not isinstance(value_, (str, int)):
            raise TypeError(f"ERROR : {value_} 不是字符串或整形数据")
        _sheetCfgList = self.getCfgList(excelName_, sheetName_)
        _backSheetCfgList = []
        for _i in range(len(_sheetCfgList)):
            _sheetCfg = _sheetCfgList[_i]
            _paramValue = getattr(_sheetCfg, f'{key_}')
            if _paramValue is None:
                raise TypeError(f"ERROR : Excel {excelName_} - {sheetName_} 上没有字段 {key_} ")
            if _paramValue == value_:
                _backSheetCfgList.append(_sheetCfg)
        return _backSheetCfgList

    # 通过两个键锁定行
    def getDoubleMatchValueCfgList(self, excelName_: str, sheetName_: str, key1_: str, value1_: Union[str, int], key2_: str, value2_: Union[str, int]):
        _match_1_cfg_list = self.getMatchValueCfgList(excelName_, sheetName_, key1_, value1_)
        _backSheetCfgList = []
        for _i in range(len(_match_1_cfg_list)):
            _sheetCfg = _match_1_cfg_list[_i]
            _paramValue = getattr(_sheetCfg, f'{key2_}')
            if _paramValue is None:
                raise TypeError(f"ERROR : Excel {excelName_} - {sheetName_} 上没有字段 {key2_} ")
            if _paramValue == value2_:
                _backSheetCfgList.append(_sheetCfg)
        return _backSheetCfgList

    def getCfgList(self, excelName_: str, sheetName_: str):
        _backSheetCfgList = []
        getExcelInsFunc = getattr(self, f'get{excelName_}')
        if getExcelInsFunc is None:
            raise TypeError(f"ERROR : Excel {excelName_} 未找到")
        _excelClassIns = getExcelInsFunc()
        if _excelClassIns is None:
            raise TypeError(f"ERROR : Excel {excelName_} 找到，但是创建对象失败")
        _sheetCfgList = getattr(_excelClassIns, f'{sheetName_}')
        if _sheetCfgList is None:
            raise TypeError(f"ERROR : Excel {excelName_} - {sheetName_} 未找到")
        return _sheetCfgList

    # 获取指定 表中 指定字段的 值范围
    def getValueListForKey(self, excelName_: str, sheetName_: str, key_: str):
        _valueList = []
        _cfgList: list = self.getCfgList(excelName_, sheetName_)
        for _i in range(len(_cfgList)):
            _cfg = _cfgList[_i]
            _paramValue = getattr(_cfg, f'{key_}')
            if _paramValue is None:
                raise TypeError(f"ERROR : Excel {excelName_} - {sheetName_} 上没有字段 {key_} ")
            _type = type(_paramValue)
            if _type == list:
                _valueList += _paramValue
            else:
                _valueList.append(_paramValue)
        return list(set(_valueList))  # 去重返回

    # 获取指定 键的值 对应其所属id列表 的字典.
    # idx_ 用于指定数组时（指明三元组中id是第几项时）。
    def get_value_idList_dict(self, excelName_: str, sheetName_: str, key_: str, idx_: int = -1):
        _value_idList_dict = {}  # 同一个值可能在多行中使用，记录这些行的Id
        _cfgList: list = self.getCfgList(excelName_, sheetName_)
        for _i in range(len(_cfgList)):
            _cfg = _cfgList[_i]
            _paramValue = getattr(_cfg, f'{key_}')
            if _paramValue is None:
                raise TypeError(f"ERROR : Excel {excelName_} - {sheetName_} 上没有字段 {key_} ")
            _type = type(_paramValue)
            if _type == list:
                if idx_ != -1:  # 指明第几个，其他的不要
                    self.setValueIdDictList(_value_idList_dict, _paramValue[idx_], _cfg.Id)
                else:  # 不指明，全都记
                    for _iLoop in range(len(_paramValue)):
                        self.setValueIdDictList(_value_idList_dict, _paramValue[_iLoop], _cfg.Id)
            else:  # 记录值的所在行id
                self.setValueIdDictList(_value_idList_dict, _paramValue, _cfg.Id)
        # 全键去重
        for _key in _value_idList_dict:
            _value_idList_dict[_key] = list(set(_value_idList_dict[_key]))
        return _value_idList_dict

    # 一个表的值关联另一个表的某个字段时，校验另一个表的某字段是否有这个值，没有的话，提示值关联的错误
    def checkConfigRelation(self, needExcel_: str, needSheet_: str, needKey_: str, targetExcel_: str, targetSheet_: str, targetKey_: str):
        # 删除

    # 记录值和id的关系
    def setValueIdDictList(self, dict_: dict, value_: Union[str, int], id_: int):
        if value_ not in dict_:
            dict_[value_] = []
        dict_[value_].append(id_)

    def dumpRelation(self):
        _folderPath = os.path.join(self.subResPath, self.excelName, "Relation")
        folderUtils.makeSureDirIsExists(_folderPath)
        _relationDataPath = os.path.join(self.subResPath, self.excelName, "Relation", f"{self.excelName}_Relation.json")
        _relationKeyValuePath = os.path.join(self.subResPath, self.excelName, "Relation", f"{self.excelName}_Relation_KV")
        _guideRootDict = self.toDict()  # 数据关系获取
        _guideRootStr = str(json.dumps(_guideRootDict, indent=4, sort_keys=False, ensure_ascii=False))
        fileUtils.writeFileWithStr(_relationDataPath, _guideRootStr)
        fileUtils.writeFileWithStr(_relationKeyValuePath, "\n".join(dictUtils.printAsKeyValue("GameGuide", _guideRootDict, False)))

    def toDict(self):
        printUtils.pError("ERROR : 必须子类实现")
        sys.exit(1)

    # 校验 Id 是否重复
    def checkListIdDuplicate(self, dataList_: list[ConfigSheet]):
        _idCacheList = []
        for _i in range(len(dataList_)):
            _data = dataList_[_i]
            if _data.Id not in _idCacheList:
                _idCacheList.append(_data.Id)
            else:
                return False, _data.Id
        return True, -1

    # 具体业务表
    # 本地化
    def __getLocalizationByName(self, name_):
        _localizationList = self.getLocalization().Localization
        for _i in range(len(_localizationList)):
            _localization: Localization_Sheet = _localizationList[_i]
            if _localization.Name == name_:
                return _localization
        return None

    # 通过中文获取
    def getLocalizationCfgByCHN(self, chnStr_):
        _localizationList = self.getLocalization().Localization
        for _i in range(len(_localizationList)):
            _localization: Localization_Sheet = _localizationList[_i]
            if chnStr_ in _localization.CHN:
                return _localization
        return None

    def getLocalStr(self, name_):
        _localization = self.__getLocalizationByName(name_)
        if _localization:
            return _localization.CHN
        else:
            return f'{name_}'

    def getLocalStr_eng(self, name_):
        _localization = self.__getLocalizationByName(name_)
        if _localization:
            return _localization.ENG
        return f'{name_}'

    # 删


if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils
    import os

    _excelFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
    _confgBase = ConfigLogicRoot(_subSvr, _excelFolderPath, "这里只是测试API不取实际Excel")
    _buildingCfg = _confgBase.getCastleBuildingById(10601).toDict()
    _buildJson = str(json.dumps(_buildingCfg, indent=4, sort_keys=False, ensure_ascii=False))
    print(_buildJson)
