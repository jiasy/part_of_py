#!/usr/bin/env python3
import sys
import os
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import folderUtils
from utils import fileCopyUtils
from FGUI.FGUIPackage import FGUIPackage
from FGUI.FGUIComponent import FGUIComponent
from FGUI.fguiUtils import fguiUtils


class CommonResManager(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(CommonResManager, self).create()

    def destroy(self):
        super(CommonResManager, self).destroy()

    # 刷新所有同名图片，只要名称相同就直接更新到对应的fgui文件中
    def replacePicWithSameName(self, fguiAssetFolder_: str, picFolder_: str):
        # 获得 图片名称 和 图片路径 的对应关系，这里会去重。
        _pngPathDict = folderUtils.getFilePathKeyValue(picFolder_, [".png"])
        _packageNameList = folderUtils.getFolderNameListJustOneDepth(fguiAssetFolder_)
        for _i in range(len(_packageNameList)):
            _packageName = _packageNameList[_i]
            _fguiPackage = FGUIPackage(fguiAssetFolder_, _packageName)
            for _key in _fguiPackage.imageDict:
                _imageDict = _fguiPackage.imageDict[_key]
                _name = _imageDict["@name"]
                if _name in _pngPathDict:
                    _relativePath = _imageDict["@path"][1:]  # 第一位的 / 要移除，不然 os.path.join 会截断
                    _toPath = os.path.join(fguiAssetFolder_, _packageName, _relativePath, _name)
                    _fromPath = _pngPathDict[_name]
                    fileCopyUtils.copyFile(_fromPath, _toPath)
                else:
                    print(f'对应关系损坏 : {_packageName} - {_name} ')

    # 将 fgui 内的图片按照目录层级拷贝出来。
    # 第一层级 为 package
    # 之后为 Folder 的相对路径，在 package 下创建出的文件夹。如下 package/a/b/yyy.png
    # <image id="xxx" name="yyy.png" path="/a/b" scale="9grid" scale9grid="157,8,314,16"/>
    def dumpPicToFolder(self, fguiAssetFolder_: str, dumpToFolder_: str):
        _packageNameList = folderUtils.getFolderNameListJustOneDepth(fguiAssetFolder_)
        folderUtils.deleteThenCreateFolder(dumpToFolder_)  # 重新创建
        for _i in range(len(_packageNameList)):
            _packageName = _packageNameList[_i]
            _fguiPackage = FGUIPackage(fguiAssetFolder_, _packageName)
            for _key in _fguiPackage.imageDict:
                _imageDict = _fguiPackage.imageDict[_key]
                _relativePath = _imageDict["@path"][1:]  # 第一位的 / 要移除，不然 os.path.join 会截断
                _name = _imageDict["@name"]
                _fromPath = os.path.join(fguiAssetFolder_, _packageName, _relativePath, _name)
                _dumpParentFolder = os.path.join(dumpToFolder_, _packageName, _relativePath)
                folderUtils.makeSureDirIsExists(_dumpParentFolder)
                _dumpToPath = os.path.join(_dumpParentFolder, _name)
                fileCopyUtils.copyFile(_fromPath, _dumpToPath)

    # 清理 包中 不使用的图片
    def removeUselessImageInPkg(self, fguiAssetFolder_: str, pkgName_: str):
        _imagePathDict = {}
        _fguiPackage = FGUIPackage(fguiAssetFolder_, pkgName_)
        for _key in _fguiPackage.imageDict:  # 包里面的图
            _imageDict = _fguiPackage.imageDict[_key]
            _relativePath = f'{_imageDict["@path"]}{_imageDict["@name"]}'[1:]
            _imagePath = os.path.join(fguiAssetFolder_, pkgName_, _relativePath)
            if os.path.exists(_imagePath):
                _imagePathDict[_imagePath] = _imageDict["@id"]  # 标记为没有
        _useIdList = []
        for _cmpName in _fguiPackage.componentDict:
            _fguiCmp = FGUIComponent(_fguiPackage, _cmpName)
            # 设计图引用
            if "@designImage" in _fguiCmp.xmlContentDict["component"] and _fguiCmp.xmlContentDict["component"]["@designImage"] != "":
                _urlStr = _fguiCmp.xmlContentDict["component"]["@designImage"]
                _pkgId, _srcId = fguiUtils.getPkgIdAndSrcId(_urlStr)
                if _pkgId == _fguiPackage.id:  # 本包内图片
                    _useIdList.append(_srcId)  # 记录到被使用中
            # 图片引用
            _imgDictList = _fguiCmp.get_dis_image_list()
            for _i in range(len(_imgDictList)):
                _imageDict = _imgDictList[_i]
                if "@pkg" not in _imageDict:  # 本包内的图片
                    _useIdList.append(_imageDict["@src"])  # 记录到被使用中
            # loader 引用
            _loadDictList = _fguiCmp.get_dis_loader_list()
            for _i in range(len(_loadDictList)):
                _loadDict = _loadDictList[_i]
                if "@url" in _loadDict and _loadDict["@url"] != "":
                    _urlStr = _loadDict["@url"]
                    _pkgId, _srcId = fguiUtils.getPkgIdAndSrcId(_urlStr)
                    if _pkgId == _fguiPackage.id:  # 本包内图片
                        _useIdList.append(_srcId)  # 记录到被使用中

        # 遍历已有内容
        _unUseIdList = []
        for _imagePath in _imagePathDict:
            _id = _imagePathDict[_imagePath]
            if _id not in _useIdList:  # 将使用的图片打印
                _unUseIdList.append(_id)
        _fguiPackage.removeAssetByIdList(_unUseIdList)  # 移除不使用的图


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils

    _fguiAssetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")
    _pkgName = "LordInfo"
    _svr.removeUselessImageInPkg(_fguiAssetFolder, _pkgName)  # 移除包内不使用的图片
    sys.exit(1)

    # # Dump 图片到指定文件夹
    # _fguiPicDumpFolder = "/Users/nobody/Downloads/assets/"
    # _svr.dumpPicToFolder(_fguiAssetFolder, _fguiPicDumpFolder)

    # 文件夹中同名的图片直接覆盖掉工程内的同名图片
    _pngResourceFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), 'svn_repos/trunk/doc/art/UI/demo/sc/pic')
    _svr.replacePicWithSameName(_fguiAssetFolder, _pngResourceFolder)

    # # FGUI 尺寸缩小
    # _fguiProject = FGUIProject(_fguiAssetFolder, [
    #     "public_icon",
    #     "public_comp",
    #     "public_avatar",
    # ])
    # _pkgName = "HeroesHall"
    # _fguiPkg = FGUIPackage(_fguiAssetFolder, _pkgName)
    # _fguiCmp = FGUIComponent(_fguiPkg, "HeroesHallRecruitItem")
    # _fguiCmp.scaleTo(0.53)
