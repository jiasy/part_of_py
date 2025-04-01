#!/usr/bin/env python3

from base.supports.Service.ServiceManager import ServiceManager


class CodeServiceManager(ServiceManager):
    def __init__(self, app_):
        super().__init__(app_)

    def create(self):
        super(CodeServiceManager, self).create()

    def destroy(self):
        super(CodeServiceManager, self).destroy()
