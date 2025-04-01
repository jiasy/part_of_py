#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils


class CodeCreateAndFormat(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(CodeCreateAndFormat, self).create()

    def destroy(self):
        super(CodeCreateAndFormat, self).destroy()


if __name__ == '__main__':
    _svr_CodeCreateAndFormat: CodeCreateAndFormat = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_CodeCreateAndFormat.resPath))
    pyServiceUtils.printSvrCode(__file__)
