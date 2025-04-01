#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils


class SpineReverse(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(SpineReverse, self).create()

    def destroy(self):
        super(SpineReverse, self).destroy()


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
