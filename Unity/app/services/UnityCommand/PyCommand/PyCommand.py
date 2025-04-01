#!/usr/bin/env python3
# Created by nobody at 2023/12/25
from base.supports.Base.BaseInService import BaseInService
from Unity.app.services.UnityCommand.UnityCommand import UnityCommand
from utils import pyServiceUtils
from utils import fileUtils
from utils import cmdUtils
from utils import dictUtils
from utils import timeUtils
from utils import jsonUtils
from utils import printUtils
import sys
import functools
import os
import time


class PyCommand(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(PyCommand, self).create()

    def destroy(self):
        super(PyCommand, self).destroy()

    # 执行 PyCommand 中的方法，工程中必须有 PyCommand.cs
    @timeUtils.execution_time_decorator
    def runPyCommandFunc(self, unityCmdToolPath_: str, projectFolder_: str, funcName_: str, *args_):
        if not os.path.exists(projectFolder_):
            print(f"ERROR : {projectFolder_} 不存在")
            sys.exit(1)

        # 确保工程有一个最简单的 PyCommand.cs
        _pyCommandInProject = os.path.join(projectFolder_, "Assets", "Scripts", "PyCommand.cs")
        _pyCommandInSupport = os.path.join(self.subResPath, "support", "PyCommand.cs")
        if os.path.exists(_pyCommandInProject) is False:
            fileUtils.copyTo(_pyCommandInSupport, _pyCommandInProject)

        # 运行时日志清空
        _nameSpace = fileUtils.justName(projectFolder_)  # 工程所在目录名为命名空间
        _pyCommandRunTimeLogPath = os.path.join(self.subResPath, "log", f"{_nameSpace}_runtime.txt")
        _unityLogPath = os.path.join(self.subResPath, "log", f"{_nameSpace}_unity.txt")
        fileUtils.writeFileWithStr(_pyCommandRunTimeLogPath, "")  # 清空运行时日志

        # 整理向 Unity 传递的参数
        _argTxtFilePath = os.path.join(projectFolder_, "Assets/PyCommand/args.txt")  # 工程内的参数文件路径
        _argStr = '\n'.join(str(_arg) for _arg in args_)  # 拼接参数
        _argStr = f'{_pyCommandRunTimeLogPath}\n{_argStr}'  # 将运行时日志放置于首位
        print(f'参数写入文件 : {_argTxtFilePath}')
        fileUtils.writeFileWithStr(_argTxtFilePath, _argStr)  # 写入参数

        # 整理命令行
        _cmd = f"{unityCmdToolPath_}"
        _cmd = f"{_cmd} -batchmode"  # Unity在没有图形用户界面的环境中运行。
        _cmd = f"{_cmd} -nographics"  # 不启动图形界面
        _cmd = f"{_cmd} -executeMethod PyCommand.{funcName_}"  # 固定调用 PyCommand 类中的内容
        _cmd = f"{_cmd} -projectPath \"{projectFolder_}\""  # 工程路径
        _cmd = f"{_cmd} -logFile \"{_unityLogPath}\""  # 完整日志
        _cmd = f"{_cmd} -quit"  # 运行结束后关闭
        print(f'{projectFolder_} 中执行 {_cmd}')
        cmdUtils.run_command_threading(_cmd, projectFolder_, 60,
                                       "Aborting batchmode due to failure:",  # 一般是执行 Cs 报错
                                       "Aborting batchmode due to fatal error:",  # 一般是开了另外一个 Unity
                                       )  # 执行并等待结束

        # 日志打印
        _logStr = fileUtils.readFromFile(_pyCommandRunTimeLogPath)  # 获取运行时日志
        printUtils.pLog(_logStr)  # 打印运行时日志

        # 是否有错误发生
        _unityCommandLine: UnityCommand = self.belongToService
        _errorLog = _unityCommandLine.getLogFirstErrorStr(_unityLogPath)
        if _errorLog is not None:  # 有
            printUtils.pError(_errorLog)


if __name__ == '__main__':
    _subSvr_PyCommand: PyCommand = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr_PyCommand.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    from Unity.app.services.UnityCommand import UnityCommand

    _unityCommand: UnityCommand = pyServiceUtils.getSvrByName("Unity", "UnityCommand")
    _unityAppPath = _unityCommand.getUnityAppPath(2023)
    _projectPath = "/Users/nobody/Documents/develop/GitRepository/Unity_2023_2D_UPR/"

    _subSvr_PyCommand.runPyCommandFunc(_unityAppPath, _projectPath, "commandLineFunc", 1, 2)
