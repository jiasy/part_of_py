#!/usr/bin/env python3
# Created by nobody at 2023/12/11
from BB.app.services.BBTs.BBTs_Config.BBTs_Config import BBTs_Config
from Proto.app.services.ExcelDataToProtoBin.ExcelDataToProtoBin import ExcelDataToProtoBin
from Proto.app.services.ExcelToProtoStruct.ExcelToProtoStruct import ExcelToProtoStruct
from Proto.app.services.ProtoToClass.ProtoToCsClass.support.ProtoCsGlobal import ProtoCSGlobal
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import cmdUtils
from utils import folderUtils
from utils import fileUtils
import os

_folderPath = os.path.dirname(os.path.realpath(__file__))  # 当前执行目录


class ProtoToCsClass(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(ProtoToCsClass, self).create()

    def destroy(self):
        super(ProtoToCsClass, self).destroy()

    # protoFolder_ 的 proto 的根文件夹
    # protoFile_ 要生成代码的 proto 文件
    # csCodeFolder_ 为生成代码的位置
    @staticmethod
    def getCsProtocCmd(protoFolder_: str, protoFile_: str, csCodeFolder_: str):
        _cmd = f"protoc {protoFile_}"
        _cmd = f"{_cmd} -I={protoFolder_}"  # proto 的根目录，以便可以查找当期proto文件内所以引用的其他文件
        _cmd = f"{_cmd} --csharp_out {csCodeFolder_}"
        return _cmd

    def protoFolderToCsClass(self, protoFolder_: str, csCodeFolder_: str):
        # 获取 proto 文件
        from Proto.ProtoApp import ProtoApp
        _app: ProtoApp = self.app
        _protoFileDict = _app.getProtoFileDict(protoFolder_)
        for _protoFileName in _protoFileDict:
            _protoFilePath = _protoFileDict[_protoFileName]
            self.protoFileToCsClass(protoFolder_, _protoFilePath, csCodeFolder_)

    # 生成代码到自定的文件夹
    def protoFileToCsClass(self, protoFolder_: str, protoFile_: str, csCodeFolder_: str):
        _cmd = self.getCsProtocCmd(protoFolder_, protoFile_, csCodeFolder_)  # 生成 cs 代码
        cmdUtils.doStrAsCmd(_cmd, protoFolder_)

    # 在指定目录创建一个 cs 命令行工程
    def createConsoleApp(self, csCodeFolder_: str, nameSpace_: str, dataCacheFolder_: str, excelFolder_: str, filterExcelNameList_: list[str], excelDataToProtoBin_: str):
        _folderName = os.path.split(csCodeFolder_)[1]
        _projFile = os.path.join(csCodeFolder_, f'{_folderName}.csproj')  # cs 工程文件
        if not os.path.exists(_projFile):
            cmdUtils.doStrAsCmd("dotnet new console", csCodeFolder_)  # 创建一个命令行工程
            cmdUtils.doStrAsCmd("dotnet add package Google.Protobuf", csCodeFolder_)  # 添加 protobuf 的支持，dotnet 会自己判断是否已经存在
            cmdUtils.doStrAsCmd("dotnet add package NUnit", csCodeFolder_)  # 添加 NUnit
            cmdUtils.doStrAsCmd("dotnet restore", csCodeFolder_)  # 还原项目依赖

        # 配置汇总
        _protoCSGlobal: ProtoCSGlobal = ProtoCSGlobal(self.app, nameSpace_, dataCacheFolder_, excelFolder_, filterExcelNameList_)
        # 配置主入口文件生成
        _nameSpaceEntryCsFile = os.path.join(csCodeFolder_, f"{nameSpace_}Entry.cs")
        fileUtils.writeFileWithStr(_nameSpaceEntryCsFile, _protoCSGlobal.toCsCode())

        from Code.app.services.CodeCreateAndFormat.CSharpFormatter import CSharpFormatter
        _csharpFormatter: CSharpFormatter = pyServiceUtils.getSubSvrByName("Code", "CodeCreateAndFormat", "CSharpFormatter")
        _csharpFormatter.formatCsFile(_nameSpaceEntryCsFile)  # 格式化文件

        # 工程入口文件生成
        programCodeStr = f'''
namespace {nameSpace_} {{
    internal static class Program {{
        private static void Main (string[] args_) {{
            ExcelConfigEntry.cacheAllData ("{excelDataToProtoBin_}");
            // 使用示例
            var _matchCardList = ExcelConfigEntry.findMatchList (ExcelConfigEntry.Card, (id_, card_) => card_.MergeCard == 10002);
            foreach (var _cardInMatch in _matchCardList) {{
                Console.WriteLine ($"_cardInMatch: {{_cardInMatch}}");
            }}
            var _card = ExcelConfigEntry.findMatchFirst (ExcelConfigEntry.Card, (id_, _card) => _card.MergeCard == 10002);
            Console.WriteLine ($"_card : {{(_card != null ? _card : "not found")}}");
        }}
    }}
}}
        '''
        fileUtils.writeFileWithStr(os.path.join(csCodeFolder_, f"Program.cs"), programCodeStr)


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr: ProtoToCsClass = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    from utils.CompanyUtil import Company_BB_Utils

    _nameSpace = "ExcelConfig"

    # 数据缓存位置
    _bbtsConfig: BBTs_Config = pyServiceUtils.getSubSvrByName("BB", "BBTs", "BBTs_Config")

    # proto 结构定义文件
    _excelToProtoStruct: ExcelToProtoStruct = pyServiceUtils.getSvrByName("Proto", "ExcelToProtoStruct")

    # 本地 bin 文件路径
    _excelDataToProtoBin: ExcelDataToProtoBin = pyServiceUtils.getSvrByName("Proto", "ExcelDataToProtoBin")
    _binFolder = os.path.join(_excelDataToProtoBin.resPath, _nameSpace)

    # excel 位置，用来获取数据
    _excelFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/design/excel")
    # 排除表
    _filterExcelNameList = ["RechargeMall", "RechargeGift", "UnitSkill", "Goddess"]

    # cs 代码
    _csCodeFolder = os.path.join(_subSvr.subResPath, _nameSpace)
    folderUtils.makeSureDirIsExists(_csCodeFolder)

    # proto 文件
    _protoFolder = os.path.join(_excelToProtoStruct.resPath, _nameSpace)

    # 通过 proto 生成 cs 代码，生成代码下放一级
    _autoCreateClassFolder = os.path.join(_csCodeFolder, "AutoCreateClass")
    folderUtils.makeSureDirIsExists(_autoCreateClassFolder)
    _subSvr.protoFolderToCsClass(_protoFolder, _autoCreateClassFolder)

    # 创建 命令行工具
    _subSvr.createConsoleApp(_csCodeFolder, _nameSpace, _bbtsConfig.subResPath, _excelFolder, _filterExcelNameList, _binFolder)
