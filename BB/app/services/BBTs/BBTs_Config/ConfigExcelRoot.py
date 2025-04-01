import sys

from BB.app.services.BBTs.BBTs_Config.BBTs_Config import BBTs_Config


class ConfigExcelRoot:
    def __init__(self, subSvr_BBTs_Config_: BBTs_Config, excelFolderPath_: str, excelName_: str):
        self.subSvr_BBTs_Config = subSvr_BBTs_Config_
        self.excelFolderPath = excelFolderPath_
        self.excelName = excelName_
        self.dataSheetDict = None
        self.sheetDataListDict = {}

    def getConfigData(self):
        if self.dataSheetDict is None:
            self.dataSheetDict = self.subSvr_BBTs_Config.createData(self.excelFolderPath, self.excelName)  # 每次都直接拿Excel内数据
        return self.dataSheetDict

    def getSheetDataList(self, sheetName_: str, SheetClass):
        if sheetName_ not in self.sheetDataListDict:  # 没记录过这个sheet的数据
            _dataSheetDict = self.getConfigData()  # 获取 excel 内的数据
            if sheetName_ not in _dataSheetDict:  # 不存在这个表就报错
                print(f"ERROR : {sheetName_} not exist.")
                sys.exit(1)
            _cfgList = _dataSheetDict[sheetName_]  # 获取表内的配置列表
            _cfgInsList = []
            for _idx in range(len(_cfgList)):
                _ins = SheetClass(self.excelName, sheetName_)  # sheet 页对应的数据类型
                _ins.init(_cfgList[_idx])
                _cfgInsList.append(_ins)
            self.sheetDataListDict[sheetName_] = _cfgInsList
        return self.sheetDataListDict[sheetName_]
