import os.path
import subprocess
from enum import Enum

from BB.app.services.BBTs.BBTs_Config.ConfgClass.CastleBlock.CastleBlock_Sheet import CastleBlock_Sheet
from BB.app.services.BBTs.BBTs_Config.ConfgClass.CastleBlock.CastleBlockType_Sheet import CastleBlockType_Sheet
from BB.app.services.BBTs.BBTs_Config.ConfigLogicRoot import ConfigLogicRoot
from utils import pyServiceUtils
from utils import folderUtils
from utils.infoUtils.InfoColor import InfoColor
from utils.infoUtils.InfoType import InfoType
from BB.app.services.BBTs.BBTs_Config.ConfgClass.ResourcePathDefine.ResourcePathDefine_Sheet import ResourcePathDefine_Sheet
from utils.CompanyUtil import Company_BB_Utils
import os

_excelFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
_fguiAssetFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets/")
# _assetListTxtPath = os.path.join(Company_BB_Utils.getSLGProjectPath(),"asset_bundle/all/iOs/processed_bundles/AssetList.txt")
_assetListTxtPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "asset_bundle/all/Android/processed_bundles/AssetList.txt")
_artFolderPath = os.path.join(Company_BB_Utils.getSLGRoot(), "DEV/projects/art/dev/project_art/dev/Assets/")
_picFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/demo/sc/pic/")


class ResourceNotFound(Enum):
    Asset_Have_Art_Have = 0
    Asset_Not_Art_Have = 1
    Asset_Not_Art_Not = 2
    Asset_Have_Art_Not = 3
    Config_Not = 4  # 配置里没有配路径


# 获取当前资源描述内容
def getAssetPathListInBundle(file_path):
    assetPathList = []
    with open(file_path, 'r') as file:
        bundle_name = None
        folderPath = None
        justFind = False
        for line in file:
            line = line.strip()
            if justFind:
                justFind = False
                folderPath = line
            else:
                if line.startswith('+'):
                    bundle_name = line[1:]
                    justFind = True
                else:
                    if bundle_name is not None:
                        assetPathList.append(folderPath + '/' + line)
    return assetPathList


# 检查 指定 名称 的 配置
def check_config_ResourcePathDefine_by_name(subSvr_, name_: str):
    _excelName = "GameGuide"  # 随意用一个
    _configLogicRoot = ConfigLogicRoot(subSvr_, _excelFolderPath, _excelName)  # 要的是基类的各种生成方法
    _assetPathList = getAssetPathListInBundle(_assetListTxtPath)  # 打出来的 Bundle 的列表
    _cfgs = _configLogicRoot.getResourcePathDefine().ResourcePathDefine  # 资源配置
    for _i in range(len(_cfgs)):
        _cfg: ResourcePathDefine_Sheet = _cfgs[_i]
        if _cfg.Name == name_:
            _type = check_config_ResourcePathDefine_single(_cfg, _assetPathList)
            if _type == ResourceNotFound.Asset_Not_Art_Have:
                _configLogicRoot.info.newLine().addInfo(f' Asset_Not_Art_Have ', InfoColor.Black, InfoColor.Red).addBlank().addInfo(f"{_cfg.Name} : {_cfg.Path}", InfoColor.Grey)
            elif _type == ResourceNotFound.Asset_Have_Art_Not:
                _configLogicRoot.info.newLine().addInfo(f' Asset_Have_Art_Not ', InfoColor.Black, InfoColor.Red).addBlank().addInfo(f"{_cfg.Name} : {_cfg.Path}", InfoColor.Grey)
            elif _type == ResourceNotFound.Asset_Not_Art_Not:
                _configLogicRoot.info.newLine().addInfo(f' Asset_Not_Art_Not ', InfoColor.Black, InfoColor.Red).addBlank().addInfo(f"{_cfg.Name} : {_cfg.Path}", InfoColor.Grey)
            elif _type == ResourceNotFound.Config_Not:
                _configLogicRoot.info.newLine().addInfo(f' Config_Not ', InfoColor.Black, InfoColor.Yellow).addBlank().addInfo(f"{_cfg.Name} : {_cfg.Path}", InfoColor.Grey)
            else:
                _configLogicRoot.info.newLine().addInfo(f' 正常 ', InfoColor.Black, InfoColor.Green).addBlank().addInfo(f"{_cfg.Name} : {_cfg.Path}", InfoColor.Grey)
    _configLogicRoot.info.doPrint(InfoType.Color)


# 检查 一条 配置
def check_config_ResourcePathDefine_single(cfg_: ResourcePathDefine_Sheet, assetPathList_: list):
    if cfg_.Path == "":
        return ResourceNotFound.Config_Not
    if cfg_.Path not in assetPathList_ and cfg_.Name != "":
        _filePath = os.path.join(_artFolderPath, cfg_.Path)
        if os.path.exists(_filePath):  # assetList 没， art 有
            return ResourceNotFound.Asset_Not_Art_Have
        else:  # asset 有 - art 没
            return ResourceNotFound.Asset_Have_Art_Not
    else:
        _filePath = os.path.join(_artFolderPath, cfg_.Path)
        if not os.path.exists(_filePath):  # asset 没 - art 没
            return ResourceNotFound.Asset_Not_Art_Not
    return ResourceNotFound.Asset_Have_Art_Have


# 检验 ResourcePathDefine
def check_config_ResourcePathDefine(subSvr_):
    _excelName = "GameGuide"  # 随意用一个
    _configLogicRoot = ConfigLogicRoot(subSvr_, _excelFolderPath, _excelName)  # 要的是基类的各种生成方法
    _assetPathList = getAssetPathListInBundle(_assetListTxtPath)  # 打出来的 Bundle 的列表
    _cfgs = _configLogicRoot.getResourcePathDefine().ResourcePathDefine  # 资源配置
    # 日志结构
    _asset_Have_Art_Not_Have_Group = _configLogicRoot.info.addGroup()  # assetList 有，art 没有
    _asset_Not_Have_Art_Have_Group = _configLogicRoot.info.addGroup()  # assetList 没有，art 有
    _asset_Not_Have_Art_Not_Have_Group = _configLogicRoot.info.addGroup()  # assetList 没有，art 没有有
    _config_Not_Group = _configLogicRoot.info.addGroup()  # assetList 没有，art 没有有
    _asset_Have_Art_Not_Have_Group.newLine().addInfo(f'asset 有 - art 没', InfoColor.Black, InfoColor.Blue)
    _asset_Not_Have_Art_Have_Group.newLine().addInfo(f'asset 没 - art 有', InfoColor.Black, InfoColor.Yellow)
    _asset_Not_Have_Art_Not_Have_Group.newLine().addInfo(f'asset 没 - art 没', InfoColor.Black, InfoColor.Red)
    _config_Not_Group.newLine().addInfo(f'config 没', InfoColor.Black, InfoColor.Magenta)
    # 比对配置 和 asset list
    for _i in range(len(_cfgs)):
        _cfg: ResourcePathDefine_Sheet = _cfgs[_i]
        _type: ResourceNotFound = check_config_ResourcePathDefine_single(_cfg, _assetPathList)
        if _type == ResourceNotFound.Asset_Not_Art_Have:
            _asset_Not_Have_Art_Have_Group.newLine().addBlank(InfoColor.Yellow).addInfo(f"{_cfg.Name} : {_cfg.Path}", InfoColor.Grey)
        elif _type == ResourceNotFound.Asset_Have_Art_Not:
            _asset_Have_Art_Not_Have_Group.newLine().addBlank(InfoColor.Blue).addInfo(f"{_cfg.Name} : {_cfg.Path}", InfoColor.Grey)
        elif _type == ResourceNotFound.Asset_Not_Art_Not:
            _asset_Not_Have_Art_Not_Have_Group.newLine().addBlank(InfoColor.Red).addInfo(f"{_cfg.Name} : {_cfg.Path}", InfoColor.Grey)
        elif _type == ResourceNotFound.Config_Not:
            _config_Not_Group.newLine().addBlank(InfoColor.Magenta).addInfo(f"{_cfg.Name} : {_cfg.Path}", InfoColor.Grey)

    # 进行打印
    _configLogicRoot.info.doPrint(InfoType.Color)


# 检查 CastleBlock
def check_config_CastleBlock(subSvr_):
    # 日志结构
    _excelName = "GameGuide"  # 随意用一个
    _configLogicRoot = ConfigLogicRoot(subSvr_, _excelFolderPath, _excelName)  # 要的是基类的各种生成方法
    _assetPathList = getAssetPathListInBundle(_assetListTxtPath)  # 打出来的 Bundle 的列表
    _castleBlockCfgs = _configLogicRoot.getCastleBlock().CastleBlock  #
    _resourcePathDefineCfgs = _configLogicRoot.getResourcePathDefine().ResourcePathDefine  # 资源配置
    for _i in range(len(_castleBlockCfgs)):
        _castleBlockCfg: CastleBlock_Sheet = _castleBlockCfgs[_i]
        _castleBlockTypeCfg: CastleBlockType_Sheet = _configLogicRoot.getCastleBlockTypeById(_castleBlockCfg.Type)
        _findBool = False
        for _iLoop in range(len(_resourcePathDefineCfgs)):
            _resourcePathDefineCfg: ResourcePathDefine_Sheet = _resourcePathDefineCfgs[_iLoop]
            if _resourcePathDefineCfg.Name == _castleBlockTypeCfg.Model:
                _findBool = True
                _type: ResourceNotFound = check_config_ResourcePathDefine_single(_resourcePathDefineCfg, _assetPathList)
                if _type is not ResourceNotFound.Asset_Have_Art_Have:
                    _configLogicRoot.info.newLine().addInfo(f' {_castleBlockCfg.Id} - {_castleBlockTypeCfg.Model} ', InfoColor.Black, InfoColor.Red).addBlank().addInfo(str(_type), InfoColor.Red)
        if _findBool is False:
            _configLogicRoot.info.newLine().addInfo(f' {_castleBlockCfg.Id} - {_castleBlockTypeCfg.Model} ', InfoColor.Black, InfoColor.Red).addBlank().addInfo(f"ResourcePathDefine 没有 {_castleBlockTypeCfg.Model}", InfoColor.Red)
    # 进行打印
    _configLogicRoot.info.doPrint(InfoType.Color)


# 获取 资源图片
def openPicInFolder(picName_: str):
    _havePicPathList = folderUtils.getFileListInFolder(_picFolderPath, [".png"])
    _filePathList = folderUtils.getFileListInFolder(_picFolderPath, [".png"])
    for _i in range(len(_filePathList)):
        _filePath = _filePathList[_i]
        if picName_ in _filePath:
            # SAMPLE 启动 Finder 打开文件所在位置
            # 构建AppleScript命令
            script = f'tell application "Finder" to reveal POSIX file "{_filePath}"'
            # 执行AppleScript命令
            subprocess.run(["osascript", "-e", script])


if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    # # 检验资源
    # check_config_ResourcePathDefine(_subSvr)

    # # Finder打开图片位置
    # openPicInFolder("Ui_icon_gbtx_di")

    # # 检查 CastleBlock 相关资源
    # check_config_CastleBlock(_subSvr)

    # 检查指定资源
    check_config_ResourcePathDefine_by_name(_subSvr, "npc_guide")
