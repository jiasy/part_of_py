#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils


# 代码的结构和关系
class StructAndRelation(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(StructAndRelation, self).create()

    def destroy(self):
        super(StructAndRelation, self).destroy()


if __name__ == '__main__':
    _svr: StructAndRelation = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
