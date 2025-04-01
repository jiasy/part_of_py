#!/usr/bin/env python3
# Created by BB at 2023/5/20
import os.path
import sys

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import fileUtils
from utils import printUtils
from utils import listUtils
from Proto.util import proto_struct_3_to_2
from BB.app.services.BBTs.BBProtoStructTS import protobufStructCode, protobufToCode
from Proto.app.services.ProtoStructAnalyse import ProtoStructAnalyse


class BBProtoStructTS(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.recoverProtoFolderPath = None
        self.targetProtoFolderPath = None
        self.projectTSFolderPath = None
        self.relativeModuleFolderPath = None
        self.moduleFolderPath = None
        self.infosAndLogFolderPath = None
        self.protobufDescribeFolder = None
        self._protoStructAnalyse: ProtoStructAnalyse = None

    def create(self):
        super(BBProtoStructTS, self).create()

    def destroy(self):
        super(BBProtoStructTS, self).destroy()

    @property
    def protoStructAnalyse(self):
        if self._protoStructAnalyse is None:
            from Proto.app.services.ProtoStructAnalyse import ProtoStructAnalyse
            self._protoStructAnalyse: ProtoStructAnalyse = pyServiceUtils.getSvrByName("Proto", "ProtoStructAnalyse")
        return self._protoStructAnalyse

    def getStructCreateCode(self, structName_: str, protoNameList_: list):
        # self.targetProtoFolderPath 中 _protoNameInFolderList 指定的 proto，全部 3 转 2 放置到 self.recoverProtoFolderPath 的 moduleName_ 文件夹内，并将解析结构返回
        proto_struct_3_to_2.styleFrom3to2(
            self.targetProtoFolderPath,  # 从这里选 proto
            "printStructCreateCode",  # 指明是这个方法使用的
            protoNameList_,  # 选哪些 proto 名称 列表
            self.recoverProtoFolderPath  # 临时放置，拷贝proto的地方
        )
        # 将整个文件夹内的 proto 都解析掉
        _tableStructureStrList = self.protoStructAnalyse.analyseProtoStructureInFolder(self.recoverProtoFolderPath)
        # 在 protoNameList_ 中找到并构建 StructName_ 的，TS 中创建该结构的代码
        structTSCreateCode = protobufStructCode.getCreateStructTsCode(self.protoStructAnalyse, structName_)
        structTSDictCode = protobufStructCode.getReadStructTsCode(self.protoStructAnalyse, structName_)
        _logStr = ""
        _logStr += " - - - - - - - -\n"
        _logStr += f"{structTSCreateCode}\n"
        _logStr += " - - - - - - - -\n"
        _logStr += f"{structTSDictCode}\n"
        return _logStr

    # 在 protoNameList_ 中找 structName_ 结构，打印它的生成代码
    def printStructCreateCode(self, structName_: str, protoNameList_: list):
        _logStr = self.getStructCreateCode(structName_, protoNameList_)
        print(_logStr)

    def printProtoStruct(self, protoNameList_: list):
        print(self.getStructInfoStr("printProtoStruct", protoNameList_))

    def getStructInfoStr(self, moduleName_: str, protoNameList_: list):
        # self.targetProtoFolderPath 中 protoNameList_ 指定的 proto，全部 3 转 2 放置到 self.recoverProtoFolderPath 的 moduleName_ 文件夹内，并将解析结构返回
        proto_struct_3_to_2.styleFrom3to2(
            self.targetProtoFolderPath,  # 从这里选 proto
            moduleName_,  # 目标模块
            protoNameList_,  # 选哪些 proto 名称 列表
            self.recoverProtoFolderPath  # 临时放置，拷贝proto的地方
        )
        # 将整个文件夹内的 proto 都解析掉
        _tableStructureStrList = self.protoStructAnalyse.analyseProtoStructureInFolder(self.recoverProtoFolderPath)
        return listUtils.joinToStr(_tableStructureStrList, "\n")

    def reCreateServiceCode(self, moduleName_: str, protoNameList_: list):
        # 将 结构信息 写入 信息中的 结构信息文件
        # 删

    # 获取自己对应的资源
    # self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")


if __name__ == '__main__':
    _bbProtoStructTs: BBProtoStructTS = pyServiceUtils.getSubSvr(__file__)
    print('_bbProtoStructTs.subResPath = ' + str(_bbProtoStructTs.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils
    import os

    # sys.exit(1)

    _bbProtoStructTs.recoverProtoFolderPath = "/Users/XS/Downloads/proto/"  # proto 3 还原成 2 放置的位置
    _bbProtoStructTs.targetProtoFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "proto/protofile/net/")  # proto 文件放置位置
    _bbProtoStructTs.projectTSFolderPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/")  # TS 工程路径
    _bbProtoStructTs.relativeModuleFolderPath = "src/Game/Module/"  # 所有模块的文件夹相对 TS 的路径
    _bbProtoStructTs.infosAndLogFolderPath = os.path.join(Company_BB_Utils.getSLGRoot(), "infosAndLogs/Infos/")  # 生成代码放置路径
    _bbProtoStructTs.protobufDescribeFolder = os.path.join(Company_BB_Utils.getSLGRoot(), "infosAndLogs/ProtobufInfo/")  # proto描述文件
    _bbProtoStructTs.moduleFolderPath = os.path.join(_bbProtoStructTs.projectTSFolderPath, _bbProtoStructTs.relativeModuleFolderPath)  # 所有模块的文件夹

    # # 生成 模块代码
    # _bbProtoStructTs.reCreateServiceCode("HeroBag", ["Hero", "Common", "CommonReward"])

    # 打印 Proto 中 指定结构名的，TS创建代码
    _bbProtoStructTs.printStructCreateCode("CancelResearchReq", ["Science", "Common", "CommonReward"])

    # # 打印 模块所需的 Proto 结构
    # _bbProtoStructTs.printProtoStruct(["Castle"])
