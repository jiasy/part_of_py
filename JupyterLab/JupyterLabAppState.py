#!/usr/bin/env python3
from base.supports.App.AppState import AppState
import os


class JupyterLabAppState(AppState):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(JupyterLabAppState, self).create()

    def destroy(self):
        super(JupyterLabAppState, self).destroy()

    def initAppState(self):
        return

