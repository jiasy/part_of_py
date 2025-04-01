#!/usr/bin/env python3
from base.supports.App.AppState import AppState
import os


class GamePlayAppState(AppState):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(GamePlayAppState, self).create()

    def destroy(self):
        super(GamePlayAppState, self).destroy()

    def initAppState(self):
        return
