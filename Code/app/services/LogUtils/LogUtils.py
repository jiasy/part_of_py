#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils


class LogUtils(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(LogUtils, self).create()

    def destroy(self):
        super(LogUtils, self).destroy()


if __name__ == '__main__':
    _svr_LogUtils: LogUtils = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_LogUtils.resPath))
    pyServiceUtils.printSvrCode(__file__)
