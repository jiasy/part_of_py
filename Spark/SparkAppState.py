#!/usr/bin/env python3
from base.supports.App.AppState import AppState
import os


class SparkAppState(AppState):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(SparkAppState, self).create()

    def destroy(self):
        super(SparkAppState, self).destroy()

    def initAppState(self):
        self.appStateDict["Presto"] = ["Presto"]
