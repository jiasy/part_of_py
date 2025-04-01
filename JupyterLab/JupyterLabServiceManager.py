#!/usr/bin/env python3

from base.supports.Service.ServiceManager import ServiceManager
import os


class JupyterLabServiceManager(ServiceManager):
    def __init__(self, app_):
        super().__init__(app_)

    def create(self):
        super(JupyterLabServiceManager, self).create()

    def destroy(self):
        super(JupyterLabServiceManager, self).destroy()
