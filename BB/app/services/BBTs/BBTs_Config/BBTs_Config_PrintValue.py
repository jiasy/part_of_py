from BB.app.services.BBTs.BBTs_Config.ConfigLogicRoot import ConfigLogicRoot
from utils import pyServiceUtils

from utils.CompanyUtil import Company_BB_Utils
import os

_excelFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    _excelName = "GameGuide"
    # 数据关系获取
    _configLogicRoot = ConfigLogicRoot(_subSvr, _excelFolderPath, _excelName)

    _localStr = _configLogicRoot.getLocalStr_eng("tech_ui_26")
    print('_localStr = ' + str(_localStr))
    from BB.app.services.BBTs.BBTs_Config.ConfgClass.ResourcePathDefine.ResourcePathDefine_Sheet import ResourcePathDefine_Sheet

    # 获取资源路径信息
    _config: ResourcePathDefine_Sheet = _configLogicRoot.getMatchValueCfgList("ResourcePathDefine", "ResourcePathDefine", "Name", "Effect_UI_HeroBag_03")[0]
    print(_config.Path)
