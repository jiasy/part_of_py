#!/usr/bin/env python3
from base.supports.App.AppState import AppState
import os


class UnityAppState(AppState):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(UnityAppState, self).create()

    def destroy(self):
        super(UnityAppState, self).destroy()

    def initAppState(self):
        self.appStateDict["UnityCSharpAnalyse"] = ["UnityCSharpAnalyse"]
        self.appStateDict["UnityLuaAnalyse"] = ["UnityLuaAnalyse"]
        self.appStateDict["UnityPrefabAnalyse"] = ["UnityPrefabAnalyse"]
        self.appStateDict["CSharpUML"] = ["CSharpUML"]
