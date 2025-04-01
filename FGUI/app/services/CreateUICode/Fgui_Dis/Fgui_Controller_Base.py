from FGUI.FGUIComponent import FGUIComponent

import sys


class Fgui_Controller_Base:
    def __init__(self, ctrlDict_: dict, fguiCmp_: FGUIComponent):
        self.ctrlDict = ctrlDict_
        self.fguiCmp = fguiCmp_

    def get_code_define(self) -> str:
        print(f"ERROR : {self.fguiCmp.pkgName} - {self.fguiCmp.cmpName} - 必须由子类实现，且不要 super(). 来调用")
        sys.exit(1)

    # 初始化代码
    def get_code_init(self) -> str:
        print(f"ERROR : {self.fguiCmp.pkgName} - {self.fguiCmp.cmpName} - 必须由子类实现，且不要 super(). 来调用")
        sys.exit(1)

    def getName(self):
        if "@name" in self.ctrlDict:
            return self.ctrlDict["@name"]
        return None
