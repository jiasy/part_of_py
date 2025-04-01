#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils


class BBLua(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(BBLua, self).create()

    def destroy(self):
        super(BBLua, self).destroy()


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
