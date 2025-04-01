#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import cmdUtils
import os


class ApkRebuild(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(ApkRebuild, self).create()

    def destroy(self):
        super(ApkRebuild, self).destroy()

    # 装工具
    def glviewApk(self):
        _glviewApkPath = os.path.join(self.resPath, "com.realtechvr. -01-22.apk")
        cmdUtils.doCmdAndGetPiplineList('adb', 'install', _glviewApkPath)


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)

    # # 装工具
    # _svr.glviewApk()
