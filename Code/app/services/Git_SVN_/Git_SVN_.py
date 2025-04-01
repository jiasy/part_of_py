#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils


class Git_SVN_(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(Git_SVN_, self).create()

    def destroy(self):
        super(Git_SVN_, self).destroy()


if __name__ == '__main__':
    _svr_Git_SVN_: Git_SVN_ = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_Git_SVN_.resPath))
    pyServiceUtils.printSvrCode(__file__)
