#!/usr/bin/env python3
from base.supports.App.AppState import AppState
import os


class CodeAppState(AppState):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(CodeAppState, self).create()

    def destroy(self):
        super(CodeAppState, self).destroy()

    def initAppState(self):
        return
