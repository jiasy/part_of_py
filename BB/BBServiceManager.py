#!/usr/bin/env python3

from base.supports.Service.ServiceManager import ServiceManager
import os


class BBServiceManager(ServiceManager):
    def __init__(self, app_):
        super().__init__(app_)

    def create(self):
        super(BBServiceManager, self).create()

    def destroy(self):
        super(BBServiceManager, self).destroy()
