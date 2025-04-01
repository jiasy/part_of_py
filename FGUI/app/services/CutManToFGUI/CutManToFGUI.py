#!/usr/bin/env python3
import sys
import os
from PIL import Image
from FGUI.FGUIPackage import FGUIPackage
from FGUI.FGUIProject import FGUIProject
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import fileUtils
from utils import folderUtils
from utils import fileCopyUtils
from utils import xmlUtils
from utils import strUtils
from utils import printUtils
from xmljson import badgerfish as bf
from xml.etree.ElementTree import tostring
import json
from FGUI.fguiUtils import fguiUtils
import re


def split_on_first_special_char(s):
    # 遍历字符串中的每个字符
    for index, char in enumerate(s):
        # 如果字符不是字母，数字或下划线，则进行分割
        if not strUtils.isNumUnderscore(char):
            # 返回分割后的两个部分
            return (s[:index], s[index:])
    # 如果没有找到特殊字符，返回整个字符串和None
    return (s, None)


'''
main.json 的主结构，只有其 layers 有用，放置了 图层信息，其他都可以忽略
|      +--uuid
|      +--id
|      +--origin
|      +--output
|      +--detail
|      +--platform
|      +--baseDpi
|      +--assets
|      +--bounds
|      |      +--x
|      |      +--y
|      |      +--width
|      |      +--height
|      +--resolution
|      +--layers [0]
|      |      +--id
|      |      +--index
|      |      +--name
|      |      +--type
|      |      +--x
|      |      +--y
|      |      +--width
|      |      +--height

layers 中的元素，只有三种 shapeLayer、layer 为图片，textLayer 为文字

type 为 shapeLayer、layer
|      |      +--id
|      |      +--index
|      |      +--name
|      |      +--type
|      |      +--x
|      |      +--y
|      |      +--width
|      |      +--height

type 为 textLayer 时，可能的字段
|      +--id
|      +--index
|      +--name
|      +--type
|      +--x
|      +--y
|      +--width
|      +--height
|      +--solidoverlay
|      |      +--solid
|      |      |      +--color
|      |      |      +--opacity
|      |      |      +--type
|      +--stroke
|      |      +--width
|      |      +--color
|      |      +--opacity
|      |      +--alignment
|      +--dropShadow
|      |      +--horizon
|      |      +--vertical
|      |      +--spread
|      |      +--blur
|      |      +--color
|      |      +--distance
|      |      +--angle
|      |      +--opacity
|      +--textInfo
|      |      +--content
|      |      +--orientation
|      |      +--bounds
|      |      |      +--x
|      |      |      +--y
|      |      |      +--width
|      |      |      +--height
|      |      +--fontPostScriptName
|      |      +--fontName
|      |      +--fontSize
|      |      +--bold
|      |      +--italic
|      |      +--color


'''


class PicInfo:
    def __init__(self, path: str, width: int, height: int):
        self.path: str = path  # 图片路径
        self.width = width  # 宽
        self.height = height  # 高

    def getScale9(self):
        _widthPer = round(self.width * 0.5)
        _heightPer = round(self.height * 0.5)
        return f'{_widthPer - 1},{_heightPer - 1},2,2'


class CutManToFGUI(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        # 设计尺寸
        self.screenWidth = 1080
        self.screenHeight = 1920

        self.assetFolder = None  # 包放置在 FGUI 哪里

        self.originalPicFolderList = None  # 图片所在
        self.originalPicInfoDict = None  # 图片信息

        self.fguiPackage = None  # 当前包信息
        self.fontDict = None  # 字体和资源对应关系

        self.fguiProject = None

    def create(self):
        super(CutManToFGUI, self).create()

    def destroy(self):
        super(CutManToFGUI, self).destroy()

    def initPackage(self, commonPackageNameList_: list[list]):
        self.fguiProject = FGUIProject(self.assetFolder, commonPackageNameList_)

    # 计算最大最小边界
    def dealGroupRect(self, groupId_: str, groupChildDictList_: list):

        return f"{_minX},{_minY}", f"{_maxX - _minX},{_maxY - _minY}"

    def dealWithText(self, childrenCount_: int, textDict_):
        name = f"n{childrenCount_}"
        if "textInfo" not in textDict_:
            return None
        _color = textDict_['textInfo']['color']
        # 填充色
        if 'solidoverlay' in textDict_:
            if 'solid' in textDict_['solidoverlay']:
                if 'color' in textDict_['solidoverlay']['solid']:
                    _color = textDict_['solidoverlay']['solid']['color']

        # 文本
        _content = textDict_['textInfo']["content"]
        _content = strUtils.removeBlankLines(_content)

        # 字体
        _font = textDict_['textInfo']['fontPostScriptName']
        if not _font in self.fontDict:
            printUtils.pError(f"体 {_font} 资源未配置")
        _font = self.fontDict[_font]

        # 大小位置
        _fontSize = round(textDict_['textInfo']['fontSize'])

        _heightBuffer = 4
        _yBuffer = 5  # 字体偏移
        _x = textDict_['x']
        _y = textDict_['y']
        _w = round(textDict_['width'])
        _h = round(textDict_['height'])
        # 高度不够，字体会偏移
        if _h < (_fontSize + _heightBuffer * 2):
            _h = _fontSize + _heightBuffer * 2
        # 将坐标定在中心
        _x = round(_x + _w * 0.5)
        _y = round(_y + _h * 0.5) - _heightBuffer - _yBuffer
        richtext = {
            "@id": f"{name}_{self.fguiPackage.item_id_base}",
            "@name": name,
            "@xy": f"{_x},{_y}",
            "@pivot": "0.5,0.5",
            "@anchor": "true",
            "@size": f"{_w},{_h}",
            "@touchable": "false",  # 富文本是可以被点击的，绝大多数需要禁用掉
            "@font": _font,
            "@fontSize": f"{_fontSize}",
            "@color": _color,
            "@align": "center",
            "@vAlign": "middle",
            "@ubb": "true",
            # "@autoSize": "shrink",
            "@text": _content.replace("\r", "&#xA;")
        }
        # 描边
        if 'stroke' in textDict_:
            richtext['@strokeColor'] = textDict_['stroke']['color']
            richtext['@strokeSize'] = textDict_['stroke']['width']

        return richtext

    def dealWithPic(self, childrenCount_: int, picLayerDict_, moduleName_: str, uiLayerName_: str, stateName_: str):

        return _imageDict

    def createPackageWithUI(self, moduleName_: str, uiLayerToCutManJsonDict: str):
        # 获取 当前要修改的包
        self.fguiPackage = FGUIPackage(self.assetFolder, moduleName_)
        # 获取当前包信息
        if not self.fguiPackage.isNew:
            print(f"{moduleName_} 添加新内容")
        else:
            print(f"{moduleName_} 创建")
        # 创建目标文件夹
        folderUtils.makeSureDirIsExists(os.path.join(self.assetFolder, moduleName_))
        folderUtils.makeSureDirIsExists(os.path.join(self.assetFolder, moduleName_, "Texture"))
        # 切图的信息
        self.originalPicInfoDict = {}
        _filePathList = []
        for _i in range(len(self.originalPicFolderList)):
            _filePathList += folderUtils.getFileListInFolder(self.originalPicFolderList[_i], [".png"])
        for _idx in range(len(_filePathList)):
            _filePath = _filePathList[_idx]
            _im = Image.open(_filePath)
            _width, _height = _im.size
            self.originalPicInfoDict[fileUtils.justName(_filePath)] = PicInfo(_filePath, round(_width), round(_height))

        # 名称和 cutMan 切图之间的关系
        for _uiLayerName in uiLayerToCutManJsonDict:
            if not _uiLayerName.endswith("Layer"):
                printUtils.pError(f"{_uiLayerName} 不是以 Layer 结尾")
                sys.exit(1)
            # 第一个状态放置到第一位置
            _mainJsonPathList = uiLayerToCutManJsonDict[_uiLayerName]
            if not _uiLayerName in self.fguiPackage.componentDict:
                # 记录组件信息
                _component = {"@id": self.fguiPackage.get_next_item_id(), "@name": f'{_uiLayerName}.xml', "@path": "/", "@exported": "true"}
                self.fguiPackage.addComponent(_component)
            else:
                printUtils.pError(f"{_uiLayerName} 已经存在于 package.xml")
                sys.exit(1)

            _firstDesignId = None
            # 设计图垫底，取第一个就行了
            for _idx in range(len(_mainJsonPathList)):
                _mainJsonPath = _mainJsonPathList[_idx]
                _designImageFilePath = folderUtils.getFileListInFolder(os.path.join(_mainJsonPath, "assets"), [".png"])[0]
                _designImageName = fileUtils.justName(_designImageFilePath)
                fileCopyUtils.copyFile(_designImageFilePath, os.path.join(self.assetFolder, moduleName_, f"{_uiLayerName}_{_idx + 1}.png"))
                _designId = self.fguiPackage.get_next_item_id()
                _designImage = {"@id": _designId, "@name": f"{_uiLayerName}_{_idx + 1}.png", "@path": "/", }
                self.fguiPackage.addImage(_designImage)
                if _idx == 0:
                    _firstDesignId = _designId
            # UI生成
            self.addUI(moduleName_, _uiLayerName, _mainJsonPathList, _firstDesignId)
        # 保存修改后的 package.xml 信息
        self.fguiPackage.save()

    # 添加一个UI
    def addUI(self, moduleName_: str, uiLayerName_: str, mainJsonPathList_: list, designId_: int):
        # 删


    def bb_default_set(self):
        from utils.CompanyUtil import Company_BB_Utils
        # FGUI包放置的路径
        self.assetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")
        # 切图文件路径
        self.originalPicFolderList = [
            # os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/demo/sc/pic"),
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/切图素材"),
        ]
        # 字体资源关系
        self.fontDict = {
            "AlibabaPuHuiTi-Heavy": "ui://1nhs5v9yubx3z",
            "AlibabaPuHuiTi-Bold": "ui://nhs5v9yubx3y",
            "Mikado-Black": "ui://1nhs5v9yubx3z",
            "Mikado-Bold": "ui://nhs5v9yubx3y",
        }

        # 公用图片 package，排序为使用图片的优先级
        self.initPackage([
            "public_icon",
            "public_comp",
            "UiElements",
            "public_avatar",
        ])


if __name__ == '__main__':
    _cutManToFGUI: CutManToFGUI = pyServiceUtils.getSvr(__file__)
    print('_cutManToFGUI.resPath = ' + str(_cutManToFGUI.resPath))
    pyServiceUtils.printSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils

    _cutManToFGUI.bb_default_set()

    # _cutManToFGUI.createPackageWithUI("Science_01", {
    #     # "ScienceTreeLayer": [
    #     #     os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/科学院/cs_科学院_主界面"),
    #     #     os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/科学院/cs_科学院_主界面_研发中")
    #     # ],
    #     # "ScienceCanNotTipLayer": [
    #     #     os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/科学院/cs_科学院_弹框1")
    #     # ],
    #     # "ScienceCanTipLayer": [
    #     #     os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/科学院/cs_科学院_弹框2")
    #     # ],
    #     # "ScienceIngTipLayer": [
    #     #     os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/科学院/cs_科学院_弹框3")
    #     # ],
    #     # "ScienceMaxTipLayer": [
    #     #     os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/科学院/cs_科学院_弹框4")
    #     # ],
    #     # "ScienceDetail_01_Layer": [
    #     #     os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/科学院/cs_科学院_弹框5")
    #     # ],
    #     # "ScienceModify_01_1Layer": [
    #     #     os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/科学院/cs_科学院_弹框6")
    #     # ],
    # })

    _cutManToFGUI.createPackageWithUI("Science_01", {
        "_ScienceTree_Alliance_Layer": [
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/联盟科技/联盟科技_a_01"),
        ],
        "Science_Alliance_TipLayer": [
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/联盟科技/联盟科技_弹窗_a_01"),
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/联盟科技/联盟科技_弹窗_a_02"),
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/联盟科技/联盟科技_弹窗_b_01"),
        ],
        "Science_Alliance__TipLayer": [
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/联盟科技/联盟科技_弹窗_c_01"),
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/联盟科技/联盟科技_弹窗_c_02"),
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/联盟科技/联盟科技_弹窗_c_03"),
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/alpha/效果图/联盟科技/联盟科技_弹窗_c_04"),
        ],
    })
