import logging
import os
import re

import utils.printUtils
from utils import fileUtils
from utils import strUtils
from Proto.util import protobufToCodeUtils
from utils import pyServiceUtils
from Proto.app.services.ProtoStructAnalyse import ProtoStructAnalyse
from Proto.app.services.ProtoStructAnalyse.ProtoStructInfo import ProtoStructInfo
from BB.app.services.BBTs.BBProtoStructTS import protobufStructCode


# 服务器 模拟 RPC
def getMockRpcName(proto_module_, proto_func_):
    return f'onReq{strUtils.upperFirstChar(proto_module_)}{strUtils.upperFirstChar(proto_func_)}'


# 测试 RPC
def getTestRpcName(proto_module_, proto_func_):
    return f'test_{proto_module_}_{proto_func_}'


def protobuf2Code(protoStructAnalye_: ProtoStructAnalyse, moduleFolder_: str, infosFolder_: str, moduleName_: str, recoverEntryProtoPath_: str, protoDescribePath_: str, protoNameList_: list):
    # 删
