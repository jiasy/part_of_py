import sys

from FGUI.FGUIComponent import FGUIComponent
from utils import folderUtils
from FGUI.FGUIPackage import FGUIPackage
from FGUI.fguiUtils import fguiUtils


class FGUIProject:
    def __init__(self, fguiAssetFolder_: str, commonPackList_: list[str]):
        self.assetFolder = fguiAssetFolder_

        # pkg 读取
        self.pkgDict = {}  # package 字典
        folderNameList = folderUtils.getFolderNameListJustOneDepth(self.assetFolder)
        for _i in range(len(folderNameList)):
            _folderName = folderNameList[_i]
            _fguiPackage = FGUIPackage(self.assetFolder, _folderName, self)
            if _fguiPackage.isNew:  # 新建直接跳过
                continue
            self.pkgDict[_folderName] = _fguiPackage

        # 构建 共通图片 和 共通组件 缓存
        self.commonImgDictDict = {}
        self.commonCmpDictDict = {}
        self.commonPkgDict = {}
        _imageNameCachedList = []
        for _i in range(len(commonPackList_)):
            _packageName = commonPackList_[_i]  # 共同模块
            if _packageName not in self.pkgDict:
                print(f"ERROR : {_packageName} 不存在")
                sys.exit(1)
            _commonFguiPackage = self.pkgDict[_packageName]
            self.commonPkgDict[_packageName] = _commonFguiPackage  # 记录共同模块
            # 去掉已经记录的图片
            _packageImageDict = {}
            for _picName in _commonFguiPackage.imageDict:
                if not _picName in _imageNameCachedList:  # 不存在缓存才记录
                    _imageNameCachedList.append(_picName)  # 缓存图片名
                    _packageImageDict[_picName] = _commonFguiPackage.imageDict[_picName]
            # 包名对应其所持有的图片或组件对象
            _packageId = _commonFguiPackage.id
            # 构建成 包名 -> 组件、图片名 -> 信息 这样的结构
            self.commonCmpDictDict[_packageId] = _commonFguiPackage.componentDict
            self.commonImgDictDict[_packageId] = _packageImageDict

    # 从通用中拿出指定图片
    def getImageFromCommon(self, picName_: str):
        for _packageId in self.commonImgDictDict:  # 遍历包
            _packageImageDict = self.commonImgDictDict[_packageId]  # 取包中图片
            if picName_ in _packageImageDict:  # 得到信息
                return _packageId, _packageImageDict[picName_]
        return None, None


if __name__ == '__main__':
    from utils.CompanyUtil import Company_BB_Utils
    import os

    _fguiAssetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")
    _fguiProject = FGUIProject(_fguiAssetFolder, [])
    _fguiProject.checkAllCmp()  # 检查所有的组件是否是已知内容
    # _cmpDict = _fguiProject.getComponentById("30agerl3", "rein31")
    _cmpDict = _fguiProject.getComponentByUiId("l2bcd21evwu221p")
    print(f'{_cmpDict.pkgName} -> {_cmpDict.cmpName}')
    _cmpDict = _fguiProject.getComponentByUiId("n8slb2v4upuzb4t")
    print(f'{_cmpDict.pkgName} -> {_cmpDict.cmpName}')
