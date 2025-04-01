#!/usr/bin/env python3
from base.supports.App.App import App
from utils import listUtils
from utils import folderUtils
from utils import pyServiceUtils
import re
import os


class ExcelWorkFlowApp(App):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    def start(self):
        return

    def testStart(self):
        self.start()

        # self.ProtoStructAnalyse()  # 解析Proto
        # self.FileOperate()  # 文件操作
        # self.CopyFiles()  # 拷贝文件夹内容
        # self.SplitTxt()  # 切割小说文本

        # self.changeAppState("SwiftCodeAnalyse")
        # self.changeAppState("CocosCreatorCodeAnalyse") # 解析 CocosCreator的结构
        # self.changeAppState("SplitTxt")  # 切割小说文本
        # self.changeAppState("Proto")  # Proto相关工具
        # self.changeAppState("PSDAnalyse")  # PSD 工具
        return

    def ProtoStructAnalyse(self):
        from Proto.app.services.ProtoStructAnalyse import ProtoStructAnalyse
        _protoStructAnalyse: ProtoStructAnalyse = pyServiceUtils.getSvrByName("Proto", "ProtoStructAnalyse")
        _tableStructureStrList = _protoStructAnalyse.analyseProtoStructureInFolder(
            # "/Volumes/Files/develop/GitHub/PY_Service/Excel/res/services/Proto/ProtoConvert/proto/"
            "/disk/SY/protocol_farm/server/"
        )
        listUtils.printList(_tableStructureStrList)

    def FileOperate(self):
        _service = self.getSingleRunningService("FileOperate")
        # _service.removeFirstCharsInEveryLine("/Users/nobody/Desktop/BuildAndroid_Fail", 9)
        # _service.removeFirstCharsInEveryLine("/Users/nobody/Desktop/BuildAndroid_Success", 9)
        # _service.removeFirstCharsInEveryLine("/Users/nobody/Desktop/BuildIOS", 9)

        _folderPath = "/Volumes/Files/develop/selfDevelop/Swift/未命名文件夹/"
        files = os.listdir(_folderPath)
        for _file in files:
            _filePath = os.path.join(_folderPath, _file)
            if not os.path.isdir(_filePath):
                _shortPath = _filePath.split(_folderPath)[1]
                _newName = _shortPath + ".txt"
                folderUtils.renameFileInFolder(_folderPath, _shortPath, _newName)

    def CopyFiles(self):
        _service = self.getSingleRunningService("CopyFiles")
        _service.coverFiles(
            [".json"],  # 拷贝那些类型
            "/disk/SY/farm/genXml/json/",  # 从哪里拷贝
            "/disk/SY/wxGame/assets/resources/Json/",  # 拷贝去哪里
            True
        )
