#!/usr/bin/env python3
from base.supports.App.AppState import AppState


class FGUIAppState(AppState):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(FGUIAppState, self).create()

    def destroy(self):
        super(FGUIAppState, self).destroy()

    def initAppState(self):
        self.appStateDict["PackageAnalyse"] = ["PackageAnalyse"]
