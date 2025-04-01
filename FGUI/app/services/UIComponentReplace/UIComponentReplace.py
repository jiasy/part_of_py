#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import fileUtils
from utils import xmlUtils
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import os
import re
import sys
from FGUI.FGUIProject import FGUIProject
from FGUI.FGUIComponent import FGUIComponent
from FGUI.fguiUtils import fguiReplaceUtils
from FGUI.fguiUtils import fguiUtils


# 对 CutManToFGUI 的结果进行二次加工
class UIComponentReplace(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        self.assetFolder = None
        self.nameReplaceDict = None  # 指定名称替换
        self.picReplaceDict = None  # 图片替换
        self.commonPackageDict = None  # 通用包的信息
        self.fguiProject = None

    def create(self):
        super(UIComponentReplace, self).create()

    def destroy(self):
        super(UIComponentReplace, self).destroy()

    # 在 common 中 找组件
    def getCommonComponent(self, componentName_: str):
        _componentList = self.commonPackageDict["packageDescription"]["resources"]["component"]
        for _i in range(len(_componentList)):
            _component = _componentList[_i]
            if f'{componentName_}.xml' == _component["@name"]:
                return _component
        print(f"ERROR : {componentName_} 不存在")
        sys.exit(1)

    # image 转换为组件 （比如某张图就是按钮的图，那么它一定会转换成按钮）
    def imageToComponent(self, imageDict_: dict):
        # 取图片名
        _fileName = imageDict_["@fileName"]
        _fileNameSplit = str(_fileName).split("/")
        _picName = _fileNameSplit[len(_fileNameSplit) - 1].split(".png")[0]
        # 有图片替换的关系
        if _picName in self.picReplaceDict:
            _componentName = self.picReplaceDict[_picName]
            _componentInfo = self.getCommonComponent(_componentName)
            # 构建组件信息
            _componentDict = {}
            # 图片上的属性都直接平移过去
            for _key in imageDict_:
                _componentDict[_key] = imageDict_[_key]
            # 特殊的值手动再修改一遍覆新增或盖掉原有
            _compId = _componentInfo["@id"]
            _componentDict["@src"] = _compId  # 指明所用资源
            _componentDict["@fileName"] = f'{_componentName}.xml'  # 指明他是一个component
            _componentDict["@pkg"] = self.commonPackageDict["packageDescription"]["@id"]  # 指明所在包
            return "component", _componentDict
        _name = imageDict_["@name"]
        # 名称替换的关系
        for _key in self.nameReplaceDict:
            if str(_name).startswith(_key):
                if self.nameReplaceDict[_key] == "loader":
                    _loaderDict = {}
                    # 都直接平移过去
                    for _key in imageDict_:  # 图片的一些字段不要给 loader
                        if _key != "@fileName" and _key != "@aspect" and _key != "@src":
                            _loaderDict[_key] = imageDict_[_key]
                    if "@anchor" not in imageDict_ or imageDict_["@anchor"] != "true":  # 没有使用锚点
                        _x, _y, _w, _h = xmlUtils.get_fgui_xy_wh(imageDict_)  # 将其变成中心点为锚点的图片
                        _x = round(_x + _w * 0.5)
                        _y = round(_y + _h * 0.5)
                        _loaderDict["@xy"] = f"{_x},{_y}"  # 改变位置，适应新的锚点
                        _loaderDict["@pivot"] = "0.5,0.5"  # 锚点指定
                        _loaderDict["@anchor"] = "true"  # 使用锚点作为坐标位置
                    _loaderDict["@fill"] = "scale"
                    return "loader", _loaderDict
        return None, None

    # 设置公共组件所在的包
    def setCommonPackage(self, commonPackageName_: str):
        _packageXmlPath = os.path.join(self.assetFolder, commonPackageName_, 'package.xml')
        _xmlContent = fileUtils.readFromFile(_packageXmlPath)
        self.commonPackageDict = bf.data(fromstring(_xmlContent))

    # 进行组件中的各种预制替换
    def doComponentReplace(self, moduleName_: str, uiNameList_: list[str]):
        for _idx in range(len(uiNameList_)):
            _cmpXmlPath = os.path.join(self.assetFolder, moduleName_, f'{uiNameList_[_idx]}.xml')
            _cmpXmlContent = xmlUtils.xmlDictFromFile(_cmpXmlPath)
            _imgDictList = fguiUtils.getImageListFromComponent(_cmpXmlContent)
            for _i in range(len(_imgDictList)):
                _imgDict = _imgDictList[_i]
                _tarKey, _tarDict = self.imageToComponent(_imgDict)
                if _tarKey is not None:  # 从 image 变成其他东西
                    fguiReplaceUtils.replaceDict(_cmpXmlContent, _cmpXmlPath, _imgDict, _tarDict, _tarKey)


if __name__ == '__main__':
    _svr: UIComponentReplace = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)

    from utils.CompanyUtil import Company_BB_Utils
    import os

    # FGUI 资源所在的文件夹路径
    _svr.assetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")

    # 图片 和 组件 的对应关系
    _svr.picReplaceDict = {
        # 图片 和 按钮的对应关系
        "Ui_btn_return_01": "btn_return",
        "Ui_bnt_ckzjm_01": "btn_blue_ckzjm_01",
        "Ui_bnt_ckzjm_02": "btn_orange_ckzjm_02",
        "Ui_common_btn_blue_01a": "btn_blue_01a",
        "Ui_common_btn_green_01": "btn_green_01",
        "Ui_common_btn_orange_01": "btn_orange_01",
        "Ui_common_btn_orange_01b": "btn_orange_01b",
        "Ui_common_btn_purple_01a": "btn_purple_01a",
        "Ui_common_btn_purple_01b": "btn_purple_01b",
        "Ui_image_gb_01": "btn_close",
        "Ui_icon_jl_01": "btn_jl_01",
        "Ui_icon_jl_02": "btn_jl_02",
    }

    # 名称 和 组件 的对应关系
    _svr.nameReplaceDict = {
        "loader": "loader",  # 图片名为 loader_xx 的要替换成 loader
    }
    # 指定公共资源 package 名
    _svr.setCommonPackage("public_comp")

    # 替换给定的 UI 中满足条件的内容
    # _svr.doComponentReplace("Castle", [
    #     # "CastleUpgradeLayer",
    #     "CastleDetailLayer"
    # ])
    # _svr.doComponentReplace("QuickQueue", [
    #     "QuickQueueActiveLayer",
    #     "QuickQueueActiveItem",
    # ])
    # _svr.doComponentReplace("HeroBag", [
    #     "HeroInfoStatsLayer"
    # ])

    _svr.doComponentReplace("Science", [
        "ScienceLayer"
    ])
