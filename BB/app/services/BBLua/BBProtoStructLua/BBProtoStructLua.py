from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import fileUtils
from utils import strUtils
from utils import pyUtils
import re
import os


class BBProtoStructLua(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(BBProtoStructLua, self).create()

    def destroy(self):
        super(BBProtoStructLua, self).destroy()

    '''
    '''

    # 二次解析文件
    def createStructAndFuncCode(self, moduleName_: str, protoPath_: str):
        from Proto.app.services.ProtoStructAnalyse.ProtoStructInfo import ProtoStructInfo
        _protoStructAnalyse: ProtoStructInfo = pyServiceUtils.getSubSvrByName("Proto", "ProtoStructAnalyse", "ProtoStructInfo")
        _protoInfo = _protoStructAnalyse.getProtobufStruct(protoPath_)
        # 打印 proto 信息结构
        # printUtils.printPyObjAsKV(fileUtils.justName(protoPath_), _protoInfo)

        # 获取模板
        _struct_res_rsp_templete_content = fileUtils.readFromFile(
            os.path.join(self.subResPath, "struct_res_rsp_templete"))
        _struct_sync_templete_content = fileUtils.readFromFile(
            os.path.join(self.subResPath, "struct_sync_templete"))
        _func_res_rsp_templete_content = fileUtils.readFromFile(
            os.path.join(self.subResPath, "func_res_rsp_templete"))  # 有结构接收
        _func_res_rsp_templete_nil_content = fileUtils.readFromFile(
            os.path.join(self.subResPath, "func_res_rsp_templete_nil"))  # 无结构接收
        _func_sync_templete_content = fileUtils.readFromFile(
            os.path.join(self.subResPath, "func_sync_templete"))
        # 结构代码
        _struct_content = ""
        # 函数代码
        _func_content = ""

        # 生成代码
        # 再用文本的方逐行扫一遍，按照格式约定进行代码生成
        _lines = fileUtils.linesFromFileWithOutEncode(protoPath_)
        _structNameList = []
        _idx = 0
        while _idx < len(_lines):
            _line = _lines[_idx]
            _idx = _idx + 1
            if _idx == len(_lines):
                break
            # 分析当期行，得到其类型 和 proto 的使用信息
            _svrType, _proto_module, _proto_func, _req_structName, _rsp_structName = self.analyseLineNoNeedSyncStruct(_line)
            _req_structName_lua = "nil"
            _rsp_structName_lua = "nil"
            if _svrType is None:
                continue
            else:
                # 上一行为注释
                _linePrev = _lines[_idx - 2]
                if not _linePrev.startswith("//"):
                    self.raiseError(pyUtils.getCurrentRunningFunctionName(),
                                    "sync，上一行必须是注释\n" + _line + "\n" + _linePrev)
                _common = _linePrev.split("//")[1].split("\n")[0]
                if _svrType == 1:  # 1 为 req -> rsp
                    # 删
                elif _svrType == 2:  # 2 为 sync
                    # 删

                else:
                    self.raiseError(pyUtils.getCurrentRunningFunctionName(), "不可能发生")
        return _struct_content, _func_content, _structNameList

    def getProtoTable(self, protoInfo_: dict, protoName_: str):
        _tableList = protoInfo_["tableList"]  # 字段列表
        for _i in range(len(_tableList)):
            _table = _tableList[_i]
            if protoName_ == _table["protoName"]:  # 字段名
                return _table
        self.raiseError(pyUtils.getCurrentRunningFunctionName(),
                        protoInfo_["fileName"] + " 不存在 " + protoName_ + " 的结构指定"
                        )

    def getArgsStr(self, protoTable_):
        _backStr = ""
        _protoPropertyList = protoTable_["propertyList"]
        _length = len(_protoPropertyList)
        for _idx in range(_length):
            _propertyName = _protoPropertyList[_idx]["propertyName"]
            _backStr = _backStr + _propertyName + " = " + _propertyName
            if _idx != (_length - 1):
                _backStr = _backStr + ","
        return "{" + _backStr + "}"

    def analyseLineNoNeedSyncStruct(self, line_):
        # 删

    def getModuleAndFunc(self, str_: str):
        _proto_module, _proto_func = strUtils.splitToAB(str_, ".")
        if _proto_module == None:
            _proto_module, _proto_func, _temp = strUtils.splitToABC(str_, ".")
            _proto_module = _proto_module + "." + _proto_func
            _proto_func = _temp
            if _proto_module == None:
                self.raiseError(pyUtils.getCurrentRunningFunctionName(), str_ + " 无法用 . 分割")
        return _proto_module, _proto_func


if __name__ == '__main__':
    # SAMPLE - 强制类型转换
    _subSvr: BBProtoStructLua = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
