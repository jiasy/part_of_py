from FGUI.FGUIComponent import FGUIComponent
from typing import Optional
from enum import Enum
import sys


class DisType(Enum):
    NONE = 0
    Component = 1
    Graph = 2
    Group = 3
    Image = 4
    List = 5
    Loader = 6
    RichText = 7
    Text = 8


'''
    可能未实现
    GLabel
    GComboBox
    GLoader3D
    GMovieClip
    GTree
    GTreeNode
'''


class CmpExtendType(Enum):
    NONE = 0
    # xml 有节点闭合的
    Button = 1
    ProgressBar = 2
    ScrollBar = 3
    Slider = 4
    # xml 没有节点闭合
    Label = 5


class Fgui_Dis_Base:
    def __init__(self, nodeDict_: dict, fguiCmp_: FGUIComponent, type_: DisType):
        self.nodeDict = nodeDict_
        self.fguiCmp = fguiCmp_
        self.type = type_

    def getExtendTypeAsComponent(self):
        # 删

    # 类型 和 命名 匹配
    def isNameValid(self, name_: str):
        _nameLower = name_.lower()
        if self.type == DisType.Component and (_nameLower.startswith("component_") or _nameLower.startswith("cmp_")):  # 组件
            return True
        elif self.type == DisType.Component and (_nameLower.startswith("btn_") or _nameLower.startswith("toggle_") or _nameLower.startswith("check_")):  # 按钮
            return True
        elif self.type == DisType.Graph and _nameLower.startswith("graph_"):
            return True
        elif self.type == DisType.Group and _nameLower.startswith("group_"):
            return True
        elif self.type == DisType.Image and (_nameLower.startswith("image_") or _nameLower.startswith("img_")):
            return True
        elif self.type == DisType.List and _nameLower.startswith("list_"):
            return True
        elif self.type == DisType.Loader and _nameLower.startswith("loader_"):
            return True
        elif self.type == DisType.RichText and (_nameLower.startswith("richtext_") or _nameLower.startswith("rtxt_")):
            return True
        elif self.type == DisType.Text and (_nameLower.startswith("text_") or _nameLower.startswith("txt_")):
            return True
        else:
            print(f"ERROR - 名称:{name_}  和 类型 {str(self.type)} 不匹配")
            return False

    def getName(self) -> Optional[str]:  # SAMPLE 返回值类型定义，可空
        if "@name" not in self.nodeDict:
            print(f"{self.fguiCmp.pkgName} - {self.fguiCmp.cmpName} - {str(self.type)} 节点名查找失败")
            return None
        return self.nodeDict["@name"]

    # 定义
    def get_code_define(self) -> str:
        print(f"ERROR : {self.fguiCmp.pkgName} - {self.fguiCmp.cmpName} - 必须由子类实现，且不要 super(). 来调用")
        sys.exit(1)

    # 初始化代码
    def get_code_init(self) -> str:
        print(f"ERROR : {self.fguiCmp.pkgName} - {self.fguiCmp.cmpName} - 必须由子类实现，且不要 super(). 来调用")
        sys.exit(1)

    def getPkg(self) -> Optional[str]:
        if "@pkg" not in self.nodeDict:
            return None
        return self.nodeDict["@pkg"]

    def getSrc(self) -> Optional[str]:
        if "@src" not in self.nodeDict:
            return None
        return self.nodeDict["@src"]
