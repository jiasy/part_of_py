#!/usr/bin/env python3

from base.supports.Service.ServiceManager import ServiceManager


class ServerServiceManager(ServiceManager):
    def __init__(self, app_):
        super().__init__(app_)

    def create(self):
        super(ServerServiceManager, self).create()

    def destroy(self):
        super(ServerServiceManager, self).destroy()
