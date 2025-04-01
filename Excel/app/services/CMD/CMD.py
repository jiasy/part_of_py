#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService


class CMD(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(CMD, self).create()

    def destroy(self):
        super(CMD, self).destroy()
