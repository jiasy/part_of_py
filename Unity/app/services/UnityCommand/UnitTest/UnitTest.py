#!/usr/bin/env python3
# Created by nobody at 2023/12/25
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import fileUtils
from utils import cmdUtils
from utils import dictUtils
from utils import xmlUtils
from utils import jsonUtils
from utils import printUtils
import sys
import os
import time


class UnitTest(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(UnitTest, self).create()

    def destroy(self):
        super(UnitTest, self).destroy()

    # 执行 工程内 所有测试
    def runTest(self, unityCmdToolPath_: str, projectFolder_: str, testResultPath_: str, logPath_: str):
        if not os.path.exists(projectFolder_):
            print(f"ERROR : {projectFolder_} 不存在")
            sys.exit(1)
        if fileUtils.getSuffix(testResultPath_) != ".xml":
            printUtils.pError("ERROR : 结果必须是 xml 结构")
            sys.exit(1)
        _startTime = time.time()  # 记录开始时间

        _cmd = f"{unityCmdToolPath_}"
        _cmd = f"{_cmd} -runTests"
        _cmd = f"{_cmd} -batchmode"  # Unity在没有图形用户界面的环境中运行。
        _cmd = f"{_cmd} -projectPath \"{projectFolder_}\""  # 工程路径
        _cmd = f"{_cmd} -testResults \"{testResultPath_}\""  # 测试结果
        _cmd = f"{_cmd} -testPlatform playmode"  # play 模式的测试
        _cmd = f"{_cmd} -logFile \"{logPath_}\""  # 完整日志
        # _cmd = f"{_cmd} -quit"  # runTests 会自动关闭，这里不要调用，否则立刻就关闭了

        cmdUtils.doStrAsCmd(_cmd, projectFolder_, True)  # 执行 Unity 测试
        self.analyseTestResult(testResultPath_)

        _endTime = time.time()  # 记录结束时间
        _exeTime = _endTime - _startTime  # 计算执行时长
        print(f"函数执行时长：{_exeTime} 秒")

    # 分析结果，打印状态
    def analyseTestResult(self, testResultPath_: str):
        if not os.path.exists(testResultPath_):
            return
        _resultDict = xmlUtils.xmlDictFromFile(testResultPath_)
        dictUtils.showDictStructure(_resultDict)
        _testRunRoot = _resultDict["test-run"]
        _testProjectSuite = _testRunRoot["test-suite"]
        _testDllSuite = _testProjectSuite["test-suite"]
        _classSuiteList = jsonUtils.getFguiXmlDictList(_testDllSuite, "test-suite")
        printUtils.pTitleLog(f'{_testProjectSuite["@name"]} -> {_testDllSuite["@name"]}', "")
        for _classIdx in range(len(_classSuiteList)):
            _classSuite = _classSuiteList[_classIdx]
            if "failure" in _classSuite:  # 出错了
                printUtils.pTitleError(f'    {_classSuite["@name"]}', "")
            else:
                printUtils.pLog(f'    {_classSuite["@name"]}')
            _funcCaseList = jsonUtils.getFguiXmlDictList(_classSuite, "test-case")
            for _funcIdx in range(len(_funcCaseList)):
                _funcCase = _funcCaseList[_funcIdx]
                if "failure" in _funcCase:  # 出错了
                    _stackInfo = _funcCase['failure']['stack-trace']['$']
                    printUtils.pTitleError(f'        {_funcCase["@name"]}', _stackInfo)
                    _errorLines = str(_funcCase['failure']['message']['$']).split('\n')
                    for _errIdx in range(len(_errorLines)):
                        printUtils.pWarn(f'        {_errorLines[_errIdx]}')
                else:
                    printUtils.pLog(f'        {_funcCase["@name"]}')


if __name__ == '__main__':
    _subSvr_UnitTest: UnitTest = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr_UnitTest.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    from Unity.app.services.UnityCommand import UnityCommand

    _unityCommand: UnityCommand = pyServiceUtils.getSvrByName("Unity", "UnityCommand")
    _unityAppPath = _unityCommand.getUnityAppPath(2023)

    _projectPath = "/Users/nobody/Documents/develop/GitRepository/Unity_2023_2D_UPR/"
    _logPath = "/Users/nobody/Downloads/rar/UnityUnitTest/log.txt"

    # _testResultPath = "/Users/nobody/Downloads/rar/UnityUnitTest/testResult.xml"
    # _svr.runTest(_unityAppPath, _projectPath, _testResultPath, _logPath)
