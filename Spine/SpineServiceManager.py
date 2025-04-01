#!/usr/bin/env python3

from base.supports.Service.ServiceManager import ServiceManager


class SpineServiceManager(ServiceManager):
    def __init__(self, app_):
        super().__init__(app_)

    def create(self):
        super(SpineServiceManager, self).create()

    def destroy(self):
        super(SpineServiceManager, self).destroy()
