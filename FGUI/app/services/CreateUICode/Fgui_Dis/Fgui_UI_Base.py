import sys
from typing import Optional
from FGUI.FGUIComponent import FGUIComponent
from FGUI.app.services.CreateUICode.Fgui_Dis.Fgui_Controller_Base import Fgui_Controller_Base
from FGUI.app.services.CreateUICode.Fgui_Dis.Fgui_Dis_Base import Fgui_Dis_Base, DisType
from FGUI.app.services.CreateUICode.Fgui_Dis.Fgui_Transition_Base import Fgui_Transition_Base
from utils import printUtils


class Fgui_UI_Base:
    def __init__(self, fguiCmp_: FGUIComponent):
        self.fguiCmp = fguiCmp_
        self.component_list = None
        self.graph_list = None
        self.group_list = None
        self.image_list = None
        self.list_list = None
        self.loader_list = None
        self.richText_list = None
        self.text_list = None
        self.get_disObj_list()  # 获取显示对象
        self.control_list = None
        self.get_control_list()  # 获取控制器
        self.transition_list = None
        self.get_transition_list()  # 获取动画

    # 删
