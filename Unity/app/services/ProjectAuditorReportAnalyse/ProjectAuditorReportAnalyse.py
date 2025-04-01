#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import jsonUtils
from utils import sysUtils
from utils import dictUtils
from utils import fileUtils
import json
import os
import shutil

'''
Unity 官方提供的分析工具
    https://github.com/Unity-Technologies/ProjectAuditor
'''


# 分析工具的日志二次加工
class ProjectAuditorReportAnalyse(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(ProjectAuditorReportAnalyse, self).create()

    def destroy(self):
        super(ProjectAuditorReportAnalyse, self).destroy()


# 获取子服务实例，获取的过程就是创建，然后创建属性关联其引用
# self.aBC = self.getSubClassObject("ABC")
# 获取自己对应资源路径 [self.resPath 为自己对应的路径，subFolder 为相对自己路径的子目录名称]
# self.resFolder = fileUtils.getPath(self.resPath, "subFolder")

'''
通过 dictUtils.showDictStructure(...) 获得字典结构如下
+--m_Issues [0]
|      +--category
|      +--description
|      +--descriptor
|      |      +--severity
|      |      +--areas [0] -- Memory、CPU 等等，类目
|      |      |      - <str>
|      |      +--customevaluator
|      |      +--description -- 描述 
|      |      +--id
|      |      +--type
|      |      +--method
|      |      +--value
|      |      +--critical -- 严重问题
|      |      +--platforms []
|      |      +--problem
|      |      +--solution -- 解决方案
|      |      +--minimumVersion
|      |      +--maximumVersion
|      +--location
|      |      +--m_Line
|      |      +--m_Path
|      +--customProperties []
|      +--depth
'''

_unityProjectFolderPath = "/disk/XS/wp_client/"


class CodeLocation:
    def __init__(self, path_: str, line_: str):
        self.path = path_
        self.line = line_


class CodeIssuesInfo:
    # 初始化一个信息
    def __init__(self, descriptor_: dict):
        self.description = descriptor_["description"]
        self.problem = descriptor_["problem"]
        self.solution = descriptor_["solution"]
        self.area = descriptor_["areas"][0]
        self.critical = descriptor_["critical"]
        self.locationList = []

    # 添加一个代码定位
    def addLocation(self, path_: str, line_: str):
        self.locationList.append(CodeLocation(path_, line_))

    def printSelf(self):
        if self.problem == "":
            return None
        _printStr = "----------------------------------------------------------------\n"  # 万恶分割线
        _printStr += "description : " + self.description + "\n"
        _printStr += "problem     : " + self.problem + "\n"
        _printStr += "solution    : " + self.solution + "\n"
        for _idx in range(len(self.locationList)):
            _codeLocation = self.locationList[_idx]
            if fileUtils.getUpperSuffix(_codeLocation.path) == ".CS":
                _csFilePath = os.path.join(_unityProjectFolderPath, _codeLocation.path)
                if _codeLocation.path.startswith("Packages/"):
                    _printStr += "    " + _codeLocation.path + " < " + str(_codeLocation.line) + " >\n"
                else:
                    print(_csFilePath + " , " + str(_codeLocation.line))
                    _code = fileUtils.linesFromFile(_csFilePath, True)[_codeLocation.line - 1]  # 获取代码
                    _printStr += "    " + _codeLocation.path + " < " + str(_codeLocation.line) + " > : " + _code + "\n"
            else:
                _printStr += "    " + _codeLocation.path + "\n"
        return _printStr


class CodeIssuesDict:
    def __init__(self):
        self.issuesDict = {}  # 普通问题

    # 添加一个问题描述
    def addIssueDescriptor(self, descriptor_: dict, location_: dict):
        _description = descriptor_["description"]
        _problem = descriptor_["problem"]
        _solution = descriptor_["solution"]
        # 分类
        _targetDict = self.issuesDict
        # 获取 同一个 问题的总汇对象
        _key = _description + _problem + _solution
        if _key not in _targetDict:
            _targetDict[_key] = CodeIssuesInfo(descriptor_)
        # 在这个问题总汇中，记录发生问题的位置
        _codeIssuesInfo = _targetDict[_key]
        _codeIssuesInfo.addLocation(location_["m_Path"], location_["m_Line"])


# 打印指定问题
def printIssue(issueDict_: dict, areaList: list):
    _printStr = ""
    for _idx in range(len(areaList)):
        _printStr += printIssueByArea(issueDict_, areaList[_idx])
    return _printStr


# 打印指定类目
def printIssueByArea(issueDict_: dict, area_: str):
    _printStr = ""
    _printStr += "AREA : " + area_ + "\n"
    for _key in issueDict_:
        _codeIssuesInfo = issueDict_[_key]
        if _codeIssuesInfo.area == area_:
            _tempPrintStr = _codeIssuesInfo.printSelf()
            if _tempPrintStr:
                _printStr += _tempPrintStr
    return _printStr


if __name__ == '__main__':
    _reportJsonFilePath = "/Users/nobody/Downloads/project-auditor-report.json"
    _reportAnalyseFilePath = "/Users/nobody/Downloads/project-auditor-report_analyse"
    _reportDict = fileUtils.dictFromJsonFile(_reportJsonFilePath)
    _m_Issues = _reportDict["m_Issues"]
    _codeIssuesDict = CodeIssuesDict()
    _areaList = []
    for _i in range(len(_m_Issues)):
        _descriptor = _m_Issues[_i]["descriptor"]
        _location = _m_Issues[_i]["location"]
        # 类目不止一个的时候提示一下
        if len(_descriptor["areas"]) > 1:
            print("areas > 1 : " + str(json.dumps(_descriptor, indent=4, sort_keys=False, ensure_ascii=False)))
        # 记录出现的 area 类型
        _area = _descriptor["areas"][0]
        if _area not in _areaList:
            _areaList.append(_area)
        # 记录这个描述信息
        _codeIssuesDict.addIssueDescriptor(_descriptor, _location)

    # 分类目打印主要问题
    _printStr = ""
    for _i in range(len(_areaList)):
        _printStr += printIssueByArea(_codeIssuesDict.issuesDict, _areaList[_i])

    # 写入文件
    fileUtils.writeFileWithStr(_reportAnalyseFilePath, _printStr)
