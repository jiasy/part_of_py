#!/usr/bin/env python3

from Excel.ExcelBaseInService import ExcelBaseInService
from utils import pyServiceUtils
import os
from utils import sysUtils
from utils import folderUtils
from utils import fileCopyUtils
from utils import fileUtils
from utils import cmdUtils
from utils import listUtils
from Main import Main


# 打印proto的结构信息，将嵌套的内容展开，将枚举类型的键值展开

class ProtoConvert(ExcelBaseInService):
    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.funcDict = {
            "PbCreator": {
                "protoFolderPath": "proto文件路径",
                "pbFolderPath": "pb文件路径",
            },
            "PbStructure": {
                "protoFolderPath": "proto文件路径",
                "structureDescriptionFilePath": "生成结构描述文件路径",
            },
        }

    def create(self):
        super(ProtoConvert, self).create()

    def destroy(self):
        super(ProtoConvert, self).destroy()

    def PbStructure(self, dParameters_: dict):
        '''
        1.文件夹结构，必须是二级结构
        Folder                         [放置proto文件的文件夹]
        |____Type                      [proto根据功能模块分组的文件夹]
             |____xxRes.proto          [发送]
             |____xxReq.proto          [接收]
             |____xxSync.proto         [同步或其他]
        2.将文件夹内的proto文件结构整理成文本
            1.按照文件夹分类，也就是 Type 。
            2.按照后缀区分类型，也就是发送、接收、其他。
                请求种类
                    Req 为请求
                    Res 为相应
                    其他
                分组种类
                    有去有回 Req <-> Res
                    有去 Req ->
                    有回 Res <-
                    其他 Others
            3.嵌套结构会直接按照层级放置展开
            4.字段的类型代表
                <!> require
                <?> optional
                [*] 数组
            5.被嵌套的结构一定要先定义，再使用
        '''
        _protoFolderPath = sysUtils.folderPathFixEnd(dParameters_["protoFolderPath"])
        _structureDescriptionFilePathPath = dParameters_["structureDescriptionFilePath"]
        _filters = dParameters_["filters"]
        # 创建 Excel 工作流
        _appName = "ExcelWorkFlow"
        _baseServiceName = "ProtoStructAnalyse"
        _baseService = self.app.main.getAppWithService(_appName, _baseServiceName)

        _structureStrList = _baseService.analyseProtoStructureInFolder(_protoFolderPath, _filters)
        fileUtils.writeFileWithStr(
            _structureDescriptionFilePathPath,
            listUtils.joinToStr(_structureStrList, "\n")
        )

    def PbCreator(self, dParameters_: dict):
        _protoFolderPath = sysUtils.folderPathFixEnd(dParameters_["protoFolderPath"])
        _pbFolderPath = sysUtils.folderPathFixEnd(dParameters_["pbFolderPath"])
        _filePathDict = folderUtils.getFilePathKeyValue(_protoFolderPath, [".proto"])
        for _, _protoPath in _filePathDict.items():  # 每一个proto文件
            _protoShortPath = _protoPath.split(_protoFolderPath)[1]
            _pbShortPath = _protoShortPath.split(".proto")[0] + ".pb"
            _cmd = "protoc --descriptor_set_out ./{0} ./{1}".format(_pbShortPath, _protoShortPath)
            cmdUtils.doStrAsCmd(
                _cmd,
                _protoFolderPath,
                True
            )

        # 将生成出来的.pb文件拷贝到目标文件一份
        fileCopyUtils.copyFilesInFolderTo([".pb"], _protoFolderPath, _pbFolderPath, "include", True)
        folderUtils.removeFileByFilter(_protoFolderPath, [".pb"])  # 再删除刚拷贝过的.pb文件


import Main

if __name__ == "__main__":
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    # 直接复制，到新文件中，只需要改，所需参数 和 命令行参数
    _folderPath = os.path.dirname(os.path.realpath(__file__))  # 当前执行目录
    _folderSplit = os.path.split(_folderPath)  # 切目录
    _baseServiceName = os.path.split(_folderSplit[0])[1]  # 再切得到上一层文件夹名
    _subBaseInServiceName = _folderSplit[1]  # 切到的后面就是子服务名称资源路径，对应的Excel不存在

    # _functionName = "PbCreator"
    # _parameterDict = {  # 所需参数
    #     "protoFolderPath": "{resFolderPath}/proto",
    #     "pbFolderPath": "{resFolderPath}/pbCreator",
    # }

    # _functionName = "PbCreator"
    # _parameterDict = {  # 所需参数
    #     "protoFolderPath": "/disk/SY/openresty/ShunYuan/proto2/",
    #     "pbFolderPath": "/disk/SY/openresty/app/lua/protobuf/ShunYuan/",
    # }print('_tempLine = ' + str(_tempLine))

    # _functionName = "PbStructure"
    # _parameterDict = {  # 所需参数
    #     "protoFolderPath": "{resFolderPath}/proto",
    #     "structureDescriptionFilePath": "{resFolderPath}/pbStructure/structure.txt",
    # }

    _functionName = "PbStructure"
    _parameterDict = {  # 所需参数
        "protoFolderPath": "/disk/SY/protocol_farm/server/",
        "structureDescriptionFilePath": "/disk/SY/NewFarm/doc/proto结构描述",
        "filters": [],
    }

    # # 将所有 proto 模拟成一个模块
    # from utils.CompanyUtil import Company_BB_Utils
    # _targetProtoFolder = "/Users/nobody/Downloads/proto/"
    # _simulateModuleName = "TempModule"
    # _simulateModule_protoFolder = os.path.join(_targetProtoFolder, _simulateModuleName)
    # folderUtils.makeSureDirIsExists(_simulateModule_protoFolder)
    # folderUtils.convertFolderFiles(
    #     None,
    #     Company_BB_Utils.getProtobufFolderPath(),
    #     _simulateModule_protoFolder, [".proto"]
    # )
    # _parameterDict = {  # 所需参数
    #     "protoFolderPath": _targetProtoFolder,
    #     "structureDescriptionFilePath": "/Users/nobody/Downloads/protoInfo",
    #     "filters": []
    # }

    _subSvr.PbStructure(_parameterDict)

    # # 执行 代码
    # Main.excelProcessStepTest( 已经存在 :
    #     _baseServiceName,
    #     _subBaseInServiceName,
    #     _functionName,
    #     _parameterDict,
    #     {  # 命令行参数
    #         "executeType": "单体测试"
    #     }
    # )

    # 执行 对应的 Excel
    # Main.execExcelCommand(
    #     _baseServiceName,
    #     _subBaseInServiceName,
    #     _functionName,
    #     {  # 命令行参数
    #         "executeType": "单体测试"
    #     }
    # )
