#!/usr/bin/env python3
from Proto.app.services.ProtoToClass.ProtoToCsClass.ProtoToCsClass import ProtoToCsClass
from Proto.app.services.ProtoToClass.ProtoToPyClass.ProtoToPyClass import ProtoToPyClass
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils


class ProtoToClass(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        self.protoToPyClass: ProtoToPyClass = None
        self.protoToCsClass: ProtoToCsClass = None

    def create(self):
        super(ProtoToClass, self).create()

    def destroy(self):
        super(ProtoToClass, self).destroy()


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
