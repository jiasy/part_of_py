#!/usr/bin/env python3
import os.path
import sys

from FGUI.FGUIProject import FGUIProject
from FGUI.app.services.CreateUICode.Fgui_Dis_BB.Fgui_UI_BB import Fgui_UI_BB
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import dictUtils
from utils import printUtils
from utils import fileUtils


class CreateUICode(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(CreateUICode, self).create()

    def destroy(self):
        super(CreateUICode, self).destroy()


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)

    from utils.CompanyUtil import Company_BB_Utils
    import os

    _fguiAssetFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets/")
    _fguiProject = FGUIProject(_fguiAssetFolder, [])



