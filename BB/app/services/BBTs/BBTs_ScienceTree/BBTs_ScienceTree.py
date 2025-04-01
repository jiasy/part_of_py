#!/usr/bin/env python3
# Created by BB at 2023/8/31
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import fileUtils
from utils import strUtils
from FGUI.FGUIPackage import FGUIPackage
import re
import os
from utils.CompanyUtil import Company_BB_Utils


def remove_extra_spaces(s):
    return re.sub(' +', ' ', s)


fguiAssetPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")


class BBTs_ScienceTree(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(BBTs_ScienceTree, self).create()

    def destroy(self):
        super(BBTs_ScienceTree, self).destroy()

    # Excel 的Cell 复制出来的内容，整理成科技层级的二维数组
    def getTreeNodeListFromConfig(self, treeConfig_: str):
        # 删

    # 覆盖掉现有 组件内容
    def writeContentToXml(self, scienceFolderName_: str, xmlName_: str, imageAndGroupList_: list, lineBgList_: list, nodeList_: list):
        _contentStr = ""
        for _i in range(len(lineBgList_)):
            _contentStr += lineBgList_[_i] + "\n"

        for _i in range(len(imageAndGroupList_)):
            _contentStr += imageAndGroupList_[_i] + "\n"

        for _i in range(len(nodeList_)):
            _contentStr += nodeList_[_i] + "\n"
        ramdomIdStr1 = strUtils.getRandomId()[0:4]
        ramdomIdStr2 = strUtils.getRandomId()[0:4]
        _xmlStr = f'''
<?xml version="1.0" encoding="utf-8"?>
<component size="1080,1920" designImage="ui://sadadadadsad">
  <displayList>
    <list id="{ramdomIdStr1}_{ramdomIdStr2}" name="mark" xy="1370,0" size="20000,364" visible="false" rotation="90" touchable="false" layout="row" overflow="scroll" colGap="200" defaultItem="ui://asdasdsawdawda">
      <item title="1"/>
      <item title="2"/>
      <item title="3"/>
      <item title="4"/>
      <item title="5"/>
      <item title="6"/>
      <item title="7"/>
      <item title="8"/>
      <item title="9"/>
      <item title="10"/>
      <item title="11"/>
      <item title="12"/>
      <item title="13"/>
      <item title="14"/>
      <item title="15"/>
      <item title="16"/>
      <item title="17"/>
      <item title="18"/>
      <item title="19"/>
      <item title="20"/>
      <item title="21"/>
      <item title="22"/>
      <item title="23"/>
      <item title="24"/>
      <item title="25"/>
      <item title="26"/>
      <item title="27"/>
      <item title="28"/>
      <item title="29"/>
      <item title="30"/>
    </list>
    {_contentStr}
  </displayList>
</component>
'''
        _scienceFolder = os.path.join(fguiAssetPath, scienceFolderName_)
        _xmlPath = os.path.join(_scienceFolder, f"{xmlName_}.xml")
        if os.path.exists(_xmlPath):
            print(f"ERROR : 已存在 - {_xmlPath}")
        fileUtils.writeFileWithStr(_xmlPath, _xmlStr)

    # 没有关系就建立，有关系就保持
    def createPackageXmlRelation(self, moduleName_: str, xmlName_: str):
        fguiPackage = FGUIPackage(fguiAssetPath, moduleName_)
        _component = {"@id": fguiPackage.get_next_item_id(), "@name": f'{xmlName_}.xml', "@path": "/", "@exported": "true"}
        if fguiPackage.hasComponent(xmlName_) == False:
            fguiPackage.addComponent(_component)
            fguiPackage.save()

    def createScienceStructure(self, treeNodeIdFinalList_: list, ramdomIdSt_: str):
        if ramdomIdSt_ is None:
            print("ERROR : ramdomIdSt_ 未指定")
            sys.exit(1)
        centerX = 540  # 第一层，第一个点的位置
        leftX = 186
        rightX = 894
        firstY = 146
        lineInterval = 415  # 行间距
        lineBuffer = 220  # 线相对于节点的偏移
        # ramdomIdSt = strUtils.getRandomId()[0:4]
        ramdomIdSt = ramdomIdSt_
        # 节点
        node = "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"mh2442c\" fileName=\"Component/ScienceTree_01_Item.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>"
        # 线的背景
        lineBgDict = {
            "Line_1_1": "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"oaobfe5a\" fileName=\"Component/Tree/Line_1_1.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>",
            "Line_1_2": "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"oaobfe5b\" fileName=\"Component/Tree/Line_1_2.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>",
            "Line_1_3": "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"oaobfe5c\" fileName=\"Component/Tree/Line_1_3.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>",
            "Line_2_1": "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"oaobfe59\" fileName=\"Component/Tree/Line_2_1.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>",
            "Line_2_2": "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"oaobfe57\" fileName=\"Component/Tree/Line_2_2.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>",
            "Line_2_3": "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"oaobfe56\" fileName=\"Component/Tree/Line_2_3.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>",
            "Line_3_1": "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"oaobfe53\" fileName=\"Component/Tree/Line_3_1.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>",
            "Line_3_2": "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"oaobfe54\" fileName=\"Component/Tree/Line_3_2.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>",
            "Line_3_3": "        <component id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"oaobfe50\" fileName=\"Component/Tree/Line_3_3.xml\" xy=\"{x},{y}\" pivot=\"0.5,0.5\" anchor=\"true\"/>",
        }

        # 组信息
        group_2_3 = "        <group id=\"{idStr}\" name=\"{name}\" xy=\"182,{y}\" size=\"716,362\"/>"
        groupDict = {
            "Group_1_1": "        <group id=\"{idStr}\" name=\"{name}\" xy=\"536,{y}\" size=\"8,190\"/>",
            "Group_1_2": group_2_3,
            "Group_1_3": group_2_3,
            "Group_2_1": group_2_3,
            "Group_2_2": group_2_3,
            "Group_2_3": group_2_3,
            "Group_3_1": group_2_3,
            "Group_3_2": group_2_3,
            "Group_3_3": group_2_3,
        }
        # 点到点的线
        imagePtoP = "        <image id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"b591411\" fileName=\"Texture/kxy_jdt_b.png\" xy=\"{x},{y}\" pivot=\"0.5,0\" anchor=\"true\" size=\"8,362\" group=\"{group}\" rotation=\"{r}\"/>"
        # 技能点到点的线
        imageAtoP = "        <image id=\"n{id}_" + ramdomIdSt + "\" name=\"{name}\" src=\"b591411\" fileName=\"Texture/kxy_jdt_b.png\" xy=\"{x},{y}\" pivot=\"0.5,0\" anchor=\"true\" size=\"8,190\" group=\"{group}\" rotation=\"{r}\"/>"
        _id = 100

        # 输出缓存
        imageAndGroupList = []
        nodeList = []
        lineBgList = []

        for _idx in range(len(treeNodeIdFinalList_) - 1):
            # print(f"第{_idx + 1}行 ========================================")
            _currentY = firstY + lineInterval * _idx  # 当前行的位置
            _treeLineNodeList = treeNodeIdFinalList_[_idx]
            _treeLineNodeNextList = treeNodeIdFinalList_[_idx + 1]
            # print(_treeLineNodeList)
            # print(_treeLineNodeNextList)
            _lenCurrent = len(_treeLineNodeList)
            _lenNext = len(_treeLineNodeNextList)
            _id = _id + 1
            _groupId = _id  # 当前链接线创建一个组Id
            _groupIdStr = f"n{_groupId}_{ramdomIdSt}"
            _faceUpLineBuffer = 4  # 朝向上的线段的附加偏移
            for _idxLoop in range(_lenCurrent):
                _prefix = f'A{_idx + 1}'
                _id = _id + 1
                if _lenCurrent == 1:  # 中央
                    _prefix = f'{_prefix}1'
                    nodeList.append(node.format(**{"name": _prefix, "x": centerX, "y": _currentY, "id": _id}))
                    # print('中 = ' + str(_prefix))
                    if _lenNext == 1:  # 下一个也是一个
                        _prefix = f'{_prefix}P{_idx + 1}1'
                    elif _lenNext == 2:  # 对两个的是三点，居中对应第二个
                        _prefix = f'{_prefix}P{_idx + 1}2'
                    elif _lenNext == 3:  # 对三个的是三点，居中对应第二个
                        _prefix = f'{_prefix}P{_idx + 1}2'
                    imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": centerX, "y": _currentY + lineBuffer + _faceUpLineBuffer, "r": 180, "id": _id, "group": _groupIdStr}))
                elif _lenCurrent == 2:  # 两侧
                    if _idxLoop == 0:  # 右侧
                        _prefix = f'{_prefix}1'
                        nodeList.append(node.format(**{"name": _prefix, "x": rightX, "y": _currentY, "id": _id}))
                        # print('右 = ' + str(_prefix))
                        if _lenNext == 1:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        elif _lenNext == 2:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        elif _lenNext == 3:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": rightX, "y": _currentY + lineBuffer + _faceUpLineBuffer, "r": 180, "id": _id, "group": _groupIdStr}))
                    elif _idxLoop == 1:  # 左侧
                        _prefix = f'{_prefix}2'
                        nodeList.append(node.format(**{"name": _prefix, "x": leftX, "y": _currentY, "id": _id}))
                        # print('左 = ' + str(_prefix))
                        if _lenNext == 1:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        elif _lenNext == 2:
                            _prefix = f'{_prefix}P{_idx + 1}2'
                        elif _lenNext == 3:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": leftX, "y": _currentY + lineBuffer + _faceUpLineBuffer, "r": 180, "id": _id, "group": _groupIdStr}))
                elif _lenCurrent == 3:  # 三点
                    if _idxLoop == 0:  # 右侧
                        _prefix = f'{_prefix}1'
                        nodeList.append(node.format(**{"name": _prefix, "x": rightX, "y": _currentY, "id": _id}))
                        # print('右 = ' + str(_prefix))
                        if _lenNext == 1:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        elif _lenNext == 2:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        elif _lenNext == 3:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": rightX, "y": _currentY + lineBuffer + _faceUpLineBuffer, "r": 180, "id": _id, "group": _groupIdStr}))
                    elif _idxLoop == 1:  # 中央
                        _prefix = f'{_prefix}2'
                        nodeList.append(node.format(**{"name": _prefix, "x": centerX, "y": _currentY, "id": _id}))
                        # print('中 = ' + str(_prefix))
                        if _lenNext == 1:
                            _prefix = f'{_prefix}P{_idx + 1}2'
                        elif _lenNext == 2:
                            _prefix = f'{_prefix}P{_idx + 1}2'
                        elif _lenNext == 3:
                            _prefix = f'{_prefix}P{_idx + 1}2'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": centerX, "y": _currentY + lineBuffer + _faceUpLineBuffer, "r": 180, "id": _id, "group": _groupIdStr}))
                    elif _idxLoop == 2:  # 左侧
                        _prefix = f'{_prefix}3'
                        nodeList.append(node.format(**{"name": _prefix, "x": leftX, "y": _currentY, "id": _id}))
                        # print('左 = ' + str(_prefix))
                        if _lenNext == 1:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        elif _lenNext == 2:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        elif _lenNext == 3:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": leftX, "y": _currentY + lineBuffer + _faceUpLineBuffer, "r": 180, "id": _id, "group": _groupIdStr}))
            # print("----------")
            _faceDownLineBuffer = 4  # 朝向下的线段需要再向下偏移一段距离，向下为+
            for _idxLoop in range(_lenNext):
                _prefix = f'A{_idx + 2}'
                _id = _id + 1
                if _lenNext == 1:  # 中央
                    _prefix = f'{_prefix}1'
                    # print('中 = ' + str(_prefix))
                    if _lenCurrent == 1:  # 下一个也是一个
                        _prefix = f'{_prefix}P{_idx + 1}1'
                    elif _lenCurrent == 2:  # 对两个的是三点，居中对应第二个
                        _prefix = f'{_prefix}P{_idx + 1}2'
                    elif _lenCurrent == 3:  # 对三个的是三点，居中对应第二个
                        _prefix = f'{_prefix}P{_idx + 1}2'
                    imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": centerX, "y": _currentY + lineBuffer + _faceDownLineBuffer, "r": 0, "id": _id, "group": _groupIdStr}))
                elif _lenNext == 2:  # 两侧
                    if _idxLoop == 0:  # 右侧
                        _prefix = f'{_prefix}1'
                        # print('右 = ' + str(_prefix))
                        if _lenCurrent == 1:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        elif _lenCurrent == 2:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        elif _lenCurrent == 3:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": rightX, "y": _currentY + lineBuffer + _faceDownLineBuffer, "r": 0, "id": _id, "group": _groupIdStr}))
                    elif _idxLoop == 1:  # 左侧
                        _prefix = f'{_prefix}2'
                        # print('左 = ' + str(_prefix))
                        if _lenCurrent == 1:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        elif _lenCurrent == 2:
                            _prefix = f'{_prefix}P{_idx + 1}2'
                        elif _lenCurrent == 3:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": leftX, "y": _currentY + lineBuffer + _faceDownLineBuffer, "r": 0, "id": _id, "group": _groupIdStr}))
                elif _lenNext == 3:  # 三点
                    if _idxLoop == 0:  # 右侧
                        _prefix = f'{_prefix}1'
                        # print('右 = ' + str(_prefix))
                        if _lenCurrent == 1:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        elif _lenCurrent == 2:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        elif _lenCurrent == 3:
                            _prefix = f'{_prefix}P{_idx + 1}1'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": rightX, "y": _currentY + lineBuffer + _faceDownLineBuffer, "r": 0, "id": _id, "group": _groupIdStr}))
                    elif _idxLoop == 1:  # 中央
                        _prefix = f'{_prefix}2'
                        # print('中 = ' + str(_prefix))
                        if _lenCurrent == 1:
                            _prefix = f'{_prefix}P{_idx + 1}2'
                        elif _lenCurrent == 2:
                            _prefix = f'{_prefix}P{_idx + 1}2'
                        elif _lenCurrent == 3:
                            _prefix = f'{_prefix}P{_idx + 1}2'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": centerX, "y": _currentY + lineBuffer + _faceDownLineBuffer, "r": 0, "id": _id, "group": _groupIdStr}))
                    elif _idxLoop == 2:  # 左侧
                        _prefix = f'{_prefix}3'
                        # print('左 = ' + str(_prefix))
                        if _lenCurrent == 1:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        elif _lenCurrent == 2:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        elif _lenCurrent == 3:
                            _prefix = f'{_prefix}P{_idx + 1}3'
                        imageAndGroupList.append(imageAtoP.format(**{"name": _prefix, "x": leftX, "y": _currentY + lineBuffer + _faceDownLineBuffer, "r": 0, "id": _id, "group": _groupIdStr}))
            # 两层任意一个长度不为1，就要添加横线
            if _lenCurrent > 1 or _lenNext > 1:
                _id = _id + 1
                imageAndGroupList.append(imagePtoP.format(**{"name": f"P{_idx + 1}1P{_idx + 1}2", "x": 536, "y": _currentY + lineBuffer, "r": -90, "id": _id, "group": _groupIdStr}))
                _id = _id + 1
                imageAndGroupList.append(imagePtoP.format(**{"name": f"P{_idx + 1}2P{_idx + 1}3", "x": 544, "y": _currentY + lineBuffer, "r": 90, "id": _id, "group": _groupIdStr}))
            imageAndGroupList.append(groupDict[f"Group_{len(_treeLineNodeList)}_{len(_treeLineNodeNextList)}"].format(**{"name": f"AP{_idx + 1}", "y": _currentY + lineBuffer, "idStr": _groupIdStr}))
            # 线背景
            lineBgList.append(lineBgDict[f"Line_{len(_treeLineNodeList)}_{len(_treeLineNodeNextList)}"].format(**{"name": f"L{_idx + 1}", "x": centerX, "y": _currentY + lineBuffer + 2, "r": 0, "id": _id}))

        return imageAndGroupList, lineBgList, nodeList


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr_BBTs_ScienceTree: BBTs_ScienceTree = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr_BBTs_ScienceTree.subResPath = ' + str(_subSvr_BBTs_ScienceTree.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    # 根据 excel 配置，生成对应的 FGUI 界面。

    _treeConfig = '''
删
'''

    _nameIdDict = {
        "X1": "qed5",
        "X2": "qndy",
        "X3": "o3xh",
    }
    _xmlName = "FGUI组件"
    _treeNodeIdFinalList = _subSvr_BBTs_ScienceTree.getTreeNodeListFromConfig(_treeConfig)  # 内容转节点
    _imageAndGroupList, _lineBgList, _nodeList = _subSvr_BBTs_ScienceTree.createScienceStructure(_treeNodeIdFinalList, _nameIdDict[_xmlName])  # 节点转xml显示节点
    _subSvr_BBTs_ScienceTree.writeContentToXml("FGUI包", _xmlName, _imageAndGroupList, _lineBgList, _nodeList)  # xml内容拼接写入
    _subSvr_BBTs_ScienceTree.createPackageXmlRelation("FGUI包", _xmlName)  # 关联 xml 和 package
