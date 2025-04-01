#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import printUtils
from utils.infoUtils.InfoColor import InfoColor
import sys


class AppResourceAnalyse(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(AppResourceAnalyse, self).create()

    def destroy(self):
        super(AppResourceAnalyse, self).destroy()


if __name__ == '__main__':
    _svr_AppResourceAnalyse: AppResourceAnalyse = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_AppResourceAnalyse.resPath))
    pyServiceUtils.printSvrCode(__file__)
