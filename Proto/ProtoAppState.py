#!/usr/bin/env python3
from base.supports.App.AppState import AppState
import os


class ProtoAppState(AppState):
    def __init__(self, sm_):
        super().__init__(sm_)
        self.appStateDict["excelToBin"] = ["ExcelDataToProtoBin", "ExcelToProtoStruct", "ProtoToClass"]

    def create(self):
        super(ProtoAppState, self).create()

    def destroy(self):
        super(ProtoAppState, self).destroy()

    def initAppState(self):
        return
