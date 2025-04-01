#!/usr/bin/env python3
from base.supports.App.AppState import AppState

import os


class TestAppState(AppState):


    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(TestAppState, self).create()

    def destroy(self):
        super(TestAppState, self).destroy()

    def initAppState(self):
        self.appStateDict["TestTest"] = ["TestTest"]
        self.appStateDict["PYService"] = ["PYService"]
