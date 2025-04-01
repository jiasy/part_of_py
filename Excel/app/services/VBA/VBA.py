#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import excelControlUtils
from utils import folderUtils
from utils import fileUtils
from utils import fileContentOperateUtils
import os

# 本机的 PERSONAL 文件位置
_personal_XLSB_path = "/Users/nobody/Library/Group Containers/UBF8T346G9.Office/User Content.localized/Startup.localized/Excel/PERSONAL.XLSB"


class VBA(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(VBA, self).create()

    def destroy(self):
        super(VBA, self).destroy()

    # 导出 Personal 的 VBA 代码，执行过程需要依托于一个 Excel，这里是临时无用的 tempExcelPath_
    def exportPersonalVBAProjectModule(self, tempExcelPath_: str):
        excelControlUtils.exportPersonalVBAProjectModule(tempExcelPath_)
        _basFilePathList = folderUtils.getFileListInFolder(os.path.join(os.path.dirname(tempExcelPath_), "Exports"), [".bas"])
        for _idx in range(len(_basFilePathList)):
            _basFilePath = _basFilePathList[_idx]
            fileUtils.convertCodeType(_basFilePath, "gb2312", "utf-8")  # 导出的内容编码转换
            _result = fileContentOperateUtils.removeLinesWithStrList(_basFilePath, ["Attribute VB_Name = "])  # 移除导出后的第一行
            if _result is True:
                fileUtils.removeExistFile(f'{_basFilePath}.bak')  # 移除工具生成的 .bak 备份文件

    # 导入 Personal 的 VBA 代码，执行过程需要依托于一个 Excel，这里是临时无用的 tempExcelPath_
    def importPersonalVBAProjectModule(self, tempExcelPath_: str):
        _basFilePathList = folderUtils.getFileListInFolder(os.path.join(os.path.dirname(tempExcelPath_), "Exports"), [".bas"])
        _importFolderPath = os.path.join(os.path.dirname(tempExcelPath_), "Imports")  # 要导入的文件目录
        _operateByHandFileList = [
            "Sheet_CheckValues",  # 值校验
            "Sheet_ChangeValues",  # 修改表内的值
            "Sheet_WhenCellSelect",  # 当选中时参数过滤
            "VBA_Export_Import",  # 执行 导入导出类，导入时自己换自己会有问题
            "ThisWorkbook"  # 快捷键定义，需要手动放到 PERSONAL.XLSB 的 ThisWorkbook 中，在Excel启动时定义快捷键
        ]  # 不能自动操作的文件
        for _idx in range(len(_basFilePathList)):
            _basFilePath = _basFilePathList[_idx]
            if fileUtils.justName(_basFilePath) in _operateByHandFileList:  # 不能自动处理的跳过
                continue  # 不导入到 Imports 文件，就不会被Excel 导入
            _importFilePath = os.path.join(_importFolderPath, os.path.split(_basFilePath)[1])
            fileUtils.convertCodeTypeDifferentFile(
                _basFilePath,  # 将之前导出并修改的文件
                _importFilePath,  # 转码到要导入的目录内
                "utf-8",
                "gb2312"
            )  # 导出的内容编码转换
            _justName = fileUtils.justName(_basFilePath)
        excelControlUtils.importPersonVBAModule(tempExcelPath_)  # 导入所有VBA


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)

    # 临时 Excel 用来适配 excelControlUtils 目前的流程，依托于一个Excel
    folderUtils.makeSureDirIsExists(_svr.resPath)
    _tempExcelPath = os.path.join(_svr.resPath, "tempExcel.xlsm")

    # # 导出现有的 VBA
    # _svr.exportPersonalVBAProjectModule(_tempExcelPath)

    # 导入现有的 VBA，VBA 通过 VSCode 在 Excel 外面编辑，再导入回去。
    _svr.importPersonalVBAProjectModule(_tempExcelPath)
