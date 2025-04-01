#!/usr/bin/env python3
from base.supports.App.AppState import AppState
import os


class MathAppState(AppState):

    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(MathAppState, self).create()

    def destroy(self):
        super(MathAppState, self).destroy()

    def initAppState(self):
        self.appStateDict["LinearAlgebra"] = ["LinearAlgebra"]
        self.appStateDict["NumPy"] = ["NumPy"]
