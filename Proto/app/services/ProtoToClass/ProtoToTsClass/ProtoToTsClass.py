#!/usr/bin/env python3
# Created by nobody at 2024/1/23
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils


class ProtoToTsClass(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(ProtoToTsClass, self).create()

    def destroy(self):
        super(ProtoToTsClass, self).destroy()


if __name__ == '__main__':
    _subSvr_ProtoToTsClass: ProtoToTsClass = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr_ProtoToTsClass.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
