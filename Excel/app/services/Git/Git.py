#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils


class Git(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(Git, self).create()

    def destroy(self):
        super(Git, self).destroy()


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
'''
from Excel.app.services.Git import Git
_svr : Git = pyServiceUtils.getSvrByName("Excel", "Git")
'''
