#!/usr/bin/env python3
from base.supports.App.AppState import AppState
import os


class BBAppState(AppState):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(BBAppState, self).create()

    def destroy(self):
        super(BBAppState, self).destroy()

    def initAppState(self):
        return

