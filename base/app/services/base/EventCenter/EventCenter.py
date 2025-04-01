#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService

import os


class EventCenter(BaseService):


    def __init__(self, sm_):
        super().__init__(sm_)
        self.sm.ec = self

    def create(self):
        self.sm.ec = self
        super(EventCenter, self).create()

    def destroy(self):
        super(EventCenter, self).destroy()
        self.sm.ec = None
