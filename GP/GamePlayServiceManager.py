#!/usr/bin/env python3

from base.supports.Service.ServiceManager import ServiceManager


class GamePlayServiceManager(ServiceManager):
    def __init__(self, app_):
        super().__init__(app_)

    def create(self):
        super(GamePlayServiceManager, self).create()

    def destroy(self):
        super(GamePlayServiceManager, self).destroy()
