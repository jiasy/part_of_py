#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import adbUtils
from utils import sysUtils
from utils import fileUtils
from utils import cmdUtils
from utils import folderUtils
from utils import excelControlUtils
import sys
import os
import time

_pwd = sysUtils.folderPathFixEnd(os.getcwd())

_dexAndUnitList = [('FPS', '帧'), ('Object in Pool', '个'), ('Asset reference by GameObject', '个'),
                   ('SyncLoad number in current frame', '个'), ('C# Object reference by Xlua Count', '个'),
                   ('Asset reference by UI', '个'), ('Asset Count', '个'), ('Bundle Count', '个'), ('UI Count', '个'),
                   ('Total Allocated Memory', 'MB'), ('Total Reserved Memory', 'MB'), ('Temp Allocator', 'MB'),
                   ('Mono Used', 'MB'), ('Mono Heap', 'MB'), ('Lua Memory', 'MB'), ('GFX Memory', 'MB'),
                   ('Total Memory', 'MB'), ('Renderer On Cpu Time', 'MS'), ('SRP Time', 'MS'),
                   ('SRP applay shader Count', '次'), ('Standard Time', 'MS'), ('Standard applay shader Count', '次'),
                   ('SetPassCall Count', '次'), ('DrawCall Count', '次'), ('DrawCall Static Count', '次'),
                   ('DrawCall Instance Count', '次'), ('DrawCall Dynamic Count', '次'), ('Dynamic Batch Time', 'MS'),
                   ('Main Thread Time', 'MS')]


class AndroidMemoryInfo(BaseService):
    def getDataTypeLength(self):
        return 29

    def getDesByID(self, id_):
        return _dexAndUnitList[id_ - 1][0]

    def getUnitByID(self, id_):
        return _dexAndUnitList[id_ - 1][1]

    def __init__(self, sm_):
        super().__init__(sm_)
        self.colorList = []
        self.cellPixel = 16  # 一个 cell 大小（正方形）
        self.picCellWidth = 8  # 一张图横向占用 8个Cell
        self.targetSheet = None  # 要写入的 Excel sheet

    def create(self):
        super(AndroidMemoryInfo, self).create()

    def getMatrixDict(self, keyList_: list):
        _matrixDict = {}
        for _i in range(len(keyList_)):
            _matrixDict[keyList_[_i]] = []
        return _matrixDict

    def destroy(self):
        super(AndroidMemoryInfo, self).destroy()

    # 截屏
    def doScreenCap(self, logFolderPath_: str, count_: int):
        # 截屏，并保存到本地
        cmdUtils.doStrAsCmdAndGetPipeline(
            "adb exec-out screencap -p > " + os.path.join(logFolderPath_, str(count_).rjust(4, "0") + ".png"),
            _pwd
        )

    # 定时采集内存数据
    def doLogMemoryInfo(self, packageName_: str, logFolderPath_: str, intervalSecond_: int = 10,
                        needScreenCap_: bool = True):
        _pid = adbUtils.getRuntimePid(packageName_)
        # TODO CPU + GPU 的使用率
        _memCmd = adbUtils.getMemInfoCmdByPid(_pid)
        _count = 0
        _startTime = 0
        while True:
            _startTime = time.time()
            _count += 1
            _lines = cmdUtils.doStrAsCmdAndGetPipeline(_memCmd, _pwd)
            fileUtils.writeFileWithStr(
                os.path.join(logFolderPath_, str(_count).rjust(4, "0") + ".txt"),
                "\n".join(_lines)
            )
            if needScreenCap_:
                self.doScreenCap(logFolderPath_, _count)  # 再截个同名的屏
            _endTime = time.time()
            _sleepTime = float(intervalSecond_) - (_endTime - _startTime)
            if _sleepTime > 0:
                time.sleep(float(intervalSecond_) - (_endTime - _startTime))  # 去掉中间执行日志读写的耗时，确保其按指定秒数进行

    # 指定要操作的 sheet
    def setTargetSheet(self, excelPath_: str, sheetName_: str):
        self.targetSheet = excelControlUtils.openSheet(excelPath_, sheetName_)

    # 把文件夹内的图片都摆放到 sheet 中
    def addPicsToSheet(self, picFolder_: str):
        _fileWithSuffixList = folderUtils.getFilterFilesInPath(picFolder_, [".png"])
        _fileWithSuffixList = sorted(_fileWithSuffixList)
        if self.targetSheet == None:
            utils.printUtils.pError("ERROR : 先调用 setTargetSheet 设置目标 sheet")
            sys.exit(1)
        for _i in range(len(_fileWithSuffixList)):
            self.targetSheet.pictures.add(_fileWithSuffixList[_i], left=self.picCellWidth * self.cellPixel * _i, top=0)

    def getBottom(self, bottom_: list, memList_: list):
        _newBottm = []
        for _i in range(len(bottom_)):
            _newBottm.append(bottom_[_i] + memList_[_i])
        return _newBottm

    def memoryToPic(self, logFolder_: str, picFolder_: str):
        adbUtils.MemInfoMgr(logFolder_).toPic(picFolder_)
        # adbUtils.MemInfoMgr(logFolder_).printSelf()
