#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils


class BBJenkins(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(BBJenkins, self).create()

    def destroy(self):
        super(BBJenkins, self).destroy()


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
