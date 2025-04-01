#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import cmdUtils
from utils import sysUtils
import os

_pwd = sysUtils.folderPathFixEnd(os.getcwd())


class Flash2Unity(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        self.flashAppPath = "/Applications/Adobe Animate 2021/Adobe Animate 2021.app/Contents/MacOS/Adobe Animate 2021"
        # /Applications/Adobe\ Animate\ 2021/Adobe\ Animate\ 2021.app/Contents/MacOS/Adobe\ Animate\ 2021

    def create(self):
        super(Flash2Unity, self).create()

    def destroy(self):
        super(Flash2Unity, self).destroy()

    def executeJSFL(self, jsflPath_: str):
        _cmd = self.flashAppPath.replace(" ", "\ ") + " -q --run-jsfl " + jsflPath_
        print('_cmd = ' + str(_cmd))
        # cmdUtils.doStrAsCmd(_cmd, _pwd, True)


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)

    _jsflPath = "/Users/nobody/Documents/develop/GitHub/Services/PY_Service/Unity/res/services/Flash2Unity/test.jsfl"

    _svr.executeJSFL(_jsflPath)
