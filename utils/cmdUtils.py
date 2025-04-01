# !/usr/bin/env python3
import os
from utils import fileUtils
from typing import List, Tuple
from utils import listUtils
from utils import pyUtils
from utils import convertUtils
from utils import printUtils
from utils import sysUtils
import subprocess
import time
import threading
import sys
import re
import psutil

sublimeAppPath = "/Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl"

sourceCompareAppPath = "/Applications/Beyond\ Compare.app/Contents/MacOS/bcomp"

# 子线程执行脚本并获得输出
cmdThreadingSuccessMark = False


def run_command_threading_inter(cmd_, cmdExeFolder_, *args_):
    global cmdThreadingSuccessMark
    _process = subprocess.Popen(cmd_, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True, cwd=cmdExeFolder_)
    while _process.poll() is None:
        _line = _process.stdout.readline()
        if _line and _line.strip() != "":
            print('output :' + str(_line))
            for _i in range(len(args_)):
                if args_[_i] in _line:
                    cmdThreadingSuccessMark = True
    cmdThreadingSuccessMark = True


# 在 timeOut_ 之前等待输出中出现 specificText_
def run_command_threading(cmd_: str, cmdExeFolder_: str, timeOut_: int, *args_):
    global cmdThreadingSuccessMark
    cmdThreadingSuccessMark = False
    # 进程内执行
    cmd_thread = threading.Thread(target=run_command_threading_inter, args=(f'{cmd_}', cmdExeFolder_, *args_))
    cmd_thread.start()
    # 开始时间记录
    start_time = time.time()
    # 脚本执行中
    while time.time() - start_time < timeOut_ and not cmdThreadingSuccessMark:
        print(f"CMD ing ... {int(round(timeOut_ - (time.time() - start_time)))}")
        time.sleep(1)
    if cmdThreadingSuccessMark:
        print("CMD success")
        return True
    else:
        cmdThreadingSuccessMark = False
        print("CMD timeout")
        return False


def openWithSublime(path_: str):
    if not os.path.exists(path_):
        print(f"ERROR : {path_} 不存在")
        sys.exit(1)
    doStrAsCmd(f"{sublimeAppPath} {path_}", os.path.split(path_)[0], False)


# 批量比较
def openWithSourceCompareList(srcAndTarList: List[Tuple[str, str]]):
    # 先启动 app，后续的比较命令都会在这个启动的App下进行。(否则每个独立的命令都会开启关闭一个SourceCompare进程)
    subprocess.call(sourceCompareAppPath.replace("\ ", " "))
    for _i in range(len(srcAndTarList)):
        srcAndTar = srcAndTarList[_i]
        openWithSourceCompare(srcAndTar[0], srcAndTar[1])


def openWithSourceCompare(srcPath_: str, tarPath_: str):
    if not os.path.exists(srcPath_):
        print(f"ERROR : src {srcPath_} 不存在")
        sys.exit(1)
    if not os.path.exists(tarPath_):
        print(f"ERROR : tar {tarPath_} 不存在")
        sys.exit(1)
    doStrAsCmd(f"{sourceCompareAppPath} {srcPath_} {tarPath_}", os.path.split(srcPath_)[0], False)


# 将 逗号分割的字符串 加工成 参数输出,最后一个参数判断它是不是需要“'”包裹
# 将 --env DB_NAME=gitlabhq_production,DB_USER=gitlab
# 转换成--env='DB_NAME=gitlabhq_production' --env='DB_USER=gitlab'
# cmdUtils.getParameterListStr("env","DB_NAME=gitlabhq_production,DB_USER=gitlab",True)
def getParameterListStr(prefix_, listStr_, isStringBoo):
    if listStr_ == None or str(listStr_).strip() == "":
        return ""
    else:
        _strList = listStr_.split(",")
        _returnStr = ""
        for _i in range(len(_strList)):
            _returnStr += getParameterStr(prefix_, _strList[_i], isStringBoo)
        return _returnStr


# 将输入参数加工成命令行参数。
# 将 --prefix_ str_[需要引号包裹 isStringBoo = true]
# 转换成--prefix_='str_'
# cmdUtils.getParameterStr("prefix_","str_",True)
def getParameterStr(prefix_, str_, isStringBoo):
    if str_ == None or str(str_).strip() == "":
        return ""
    else:
        _returnStr = ""
        if isStringBoo:
            _returnStr = '--' + prefix_ + '=\'' + str_ + '\' '
        else:
            _returnStr = '--' + prefix_ + '=' + str_ + ' '
        return _returnStr


# 在 whichFolder_ 路径下，执行 cmdStr_ ，printPipeLines_ 为 True 并将内容输出
def doStrAsCmd(cmdStr_: str, whichFolder_: str, printPipeLines_: bool = False, inputData_: str = None):
    _tabeSpace = " " * 4
    print(f'{_tabeSpace}{whichFolder_} 中执行命令 {cmdStr_}')  # 提示正在执行
    # shell：如果该参数为 True，将通过操作系统的 shell 执行指定的命令。
    # cwd：用于设置子进程的当前目录。
    _cmdResult = subprocess.Popen(
        cmdStr_, shell=True,
        cwd=whichFolder_,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'
    )
    # 子进程的PID : _cmdResult.pid
    # 发送信号到子进程 : send_signal
    # communicate 该方法会阻塞父进程，直到子进程完成
    _out, _err = _cmdResult.communicate(inputData_)
    # 结果转换成行数组
    _pipeLines = _out.splitlines()
    if _cmdResult.returncode != 0:
        print(_tabeSpace + 'ERROR CODE : ' + str(_cmdResult.returncode))
        print(_tabeSpace + 'ERROR INFO : ' + str(_err))
        for _i in range(len(_pipeLines)):
            print(_tabeSpace * 2 + _pipeLines[_i])
        sys.exit(1)
    else:
        if printPipeLines_:  # 需要输出的话
            for _i in range(len(_pipeLines)):
                _currentPipLine = _pipeLines[_i]
                _currentPipLine = _tabeSpace * 2 + _currentPipLine
                print(_currentPipLine)
        print(_tabeSpace + "- EXECUTE END -")  # 执行结束
        return _pipeLines


# 执行 cmd 语句，并获得输出
def doStrAsCmdAndGetPipeline(cmdStr_: str, whichFolder_: str):
    _cmdResult = subprocess.Popen(cmdStr_, shell=True, cwd=whichFolder_, stdout=subprocess.PIPE, encoding='utf-8')
    _out, _err = _cmdResult.communicate()
    return _out.splitlines()


# 获取文件夹内的文件，权限信息，苹果环境下，携带@限制权限符
def showXattr(folderPath_: str):
    if sysUtils.os_is_mac():
        listUtils.printList(doStrAsCmdAndGetPipeline("ls -laeO@", folderPath_))


# 不需要指定目录的
def doCmdAndGetPiplineList(*args_):
    return subprocess.check_output(args_).decode('utf-8').split("\n")


def checkAndKillCmdList(cmdList_: list[str]):
    for _i in range(len(cmdList_)):
        _cmd = cmdList_[_i]
        if isCmdRunning(_cmd):
            print(f"kill : {_cmd}")
            killCmd(_cmd)


def killCmd(cmd_: str):
    # 寻找并关闭与给定命令相关的进程
    _proc = getCmdProcess(cmd_)
    if _proc is not None:
        _proc.terminate()
        print(f"关闭： {_proc.info['cmdline']}, PID: {_proc.pid}")
        return True
    print(f"{cmd_} 未找到")
    return False


def isCmdRunning(cmd_: str):
    _proc = getCmdProcess(cmd_)
    if _proc is not None:
        return True
    return False


def getCmdProcess(cmd_: str):
    for _proc in psutil.process_iter(["cmdline"]):
        try:
            if _proc.info["cmdline"] and cmd_ in " ".join(_proc.info["cmdline"]):
                return _proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    return None


'''
权限数字
    -rw------- (600)    只有拥有者有读写权限。
    -rw-r--r-- (644)    只有拥有者有读写权限；而属组用户和其他用户只有读权限。
    -rwx------ (700)    只有拥有者有读、写、执行权限。
    -rwxr-xr-x (755)    拥有者有读、写、执行权限；而属组用户和其他用户只有读、执行权限。
    -rwx--x--x (711)    拥有者有读、写、执行权限；而属组用户和其他用户只有执行权限。
    -rw-rw-rw- (666)    所有用户都有文件读、写权限。
    -rwxrwxrwx (777)    所有用户都有读、写、执行权限。
单组权限数字
    rwx = 111 = 7
    rw- = 110 = 6
    r-x = 101 = 5
    r-- = 100 = 4
    -wx = 011 = 3
    -w- = 010 = 2
    --x = 001 = 1
    --- = 000 = 0
第一位，mac的特殊标识
    d代表的是目录(directroy)
    -代表的是文件(regular file)
    s代表的是套字文件(socket)
    p代表的管道文件(pipe)或命名管道文件(named pipe)
    l代表的是符号链接文件(symbolic link)
    b代表的是该文件是面向块的设备文件(block-oriented device file)
    c代表的是该文件是面向字符的设备文件(charcter-oriented device file)
查权限
    ls -laeO@
    去掉mac的xattr权限，rwx -> 111 -> 7
    chmod -R 777 'file'
'''


# 移除mac的特殊权限
def removeMacXattr(filePath_: str):
    if sysUtils.os_is_mac():
        _fileNameWithSuffix = os.path.split(filePath_)[1]  # 文件名
        _fileLocateFolderPath = os.path.split(filePath_)[0]  # 文件夹
        _pipelines = doStrAsCmdAndGetPipeline("ls -laeO@", _fileLocateFolderPath)  # 打印所在文件夹的文件列表
        '''
drwxr-xr-x  14 nobody  staff  -            476 Sep 16 17:24 .
drwxr-xr-x  22 nobody  admin  -            748 Sep 16 17:30 ..
-rw-r--r--@  1 nobody  staff  hidden      6148 Sep 16 17:24 .DS_Store
    com.apple.FinderInfo	       32 
drwxr-xr-x   4 nobody  staff  -            136 Sep 14 18:07 __pycache__
-rwxr-xr-x   1 nobody  staff  -           2234 Jul 23 14:17 android.keystore
-rw-r--r--@  1 nobody  staff  -       19964258 Sep 14 18:04 apktool_2.6.0.jar
    com.apple.metadata:kMDItemWhereFroms	      469 
    com.apple.quarantine	       57 
drwxr-xr-x  15 nobody  staff  -            510 Sep 16 17:50 deapk
-rw-r--r--   1 nobody  staff  -            319 Aug 23 11:26 gol.py
-rw-r--r--   1 nobody  staff  -            685 Sep 10 15:47 gol.pyc
-rw-r--r--@  1 nobody  staff  -            205 Aug 23 11:26 log.py
    com.apple.lastuseddate#PS	       16 
-rw-r--r--   1 nobody  staff  -            599 Sep 10 15:47 log.pyc
drwxr-xr-x   3 nobody  staff  -            102 Sep 15 21:06 outputs
-rw-r--r--@  1 nobody  staff  -           1620 Sep 16 16:56 package.py
    com.apple.lastuseddate#PS	       16 
-rw-r--r--@  1 nobody  staff  -      168508929 Sep 14 09:58 富豪麻将-demo.apk
    com.apple.lastuseddate#PS	       16 
        '''
        _idx = 0
        # 查找匹配的文件路径
        while (_idx < len(_pipelines)):
            _pipeline = _pipelines[_idx]
            if _pipeline.endswith(" " + _fileNameWithSuffix):  # 找到文件所在行
                doStrAsCmd("chmod -R 666 '" + _fileNameWithSuffix + "'", _fileLocateFolderPath, True)  # 文件读写权限
                for _j in range(_idx + 1, len(_pipelines)):  # 后续有可能是权限描述
                    _pipelineFollow = _pipelines[_j]
                    _beginTimeResult = re.search(r'^\s+([a-z\.\#A-Z0-9]+)\s+([-0-9]+)', _pipelineFollow)
                    if _beginTimeResult:
                        _id = convertUtils.strToInt(_beginTimeResult.group(2))
                        if _id > 0:
                            _xattr = _beginTimeResult.group(1)
                            '''
                            xattr 命令清除 app 的拓展属性
                                com.apple.quarantine 隔离属性，阻止运行
                                -d 删除隔离属性
                                -r 文件夹递归，删除隔离属性
                                'sudo xattr -r -d com.apple.quarantine 文件路径'
                            '''
                            _cmdStr = "xattr -dr '" + _xattr + "' '" + _fileNameWithSuffix + "'"
                            doStrAsCmd(_cmdStr, _fileLocateFolderPath, True)
                        else:
                            try:
                                # 为了获取一个默认权限的版本，通过复制替换的方式来做的。
                                fileUtils.replaceFileBySelf(filePath_)
                            except Exception as _err:
                                raise pyUtils.AppError(
                                    "权限-1:\n    1.关闭Excel,后重启Finder，再次进行尝试。\n    2.拷贝出来，手动删除原有，再粘贴回去。\n" +
                                    str(_err.args)
                                )
                    else:
                        _idx = _j - 1  # 当前不是属性，下一个循环，要从不是属性的位置开始。后面加，这里要减
                        break
            _idx += 1


# 获取校验参数[参数配置是已知的，无法配置未知的参数]
def getOps(opsDefineDict_, parse_):
    # 按照参数指定设置参数解析
    for _key in opsDefineDict_:
        _val = opsDefineDict_[_key]
        parse_.add_option('', "--" + _key, dest=_key, help=_val)

    # 取得传入的参数
    _argsParseArr = parse_.parse_args()
    _opsDict = _argsParseArr[0]  # 这里参数值对应的参数名存储在这个_ops字典里

    _opsKeyValueDict = {}
    # 解析每一个参数
    for _key in opsDefineDict_:
        # 可选项的话，就忽略，进行下一个
        if _key == "__option__":
            continue
        # 输出参数中没有这个key
        if not _opsDict.__dict__[_key]:
            # 如果编辑了可选项，那么可选项内的参数缺失，只提示，不报错
            if "__option__" in opsDefineDict_ and _key in opsDefineDict_["__option__"]:
                print("WARNING : <" + _key + ":" + opsDefineDict_[_key] + "> 空参数")
            else:
                # 如果不在可选项中，那么就报错，停止进程
                printUtils.pError("ERROR : 必须有 " + _key + " -> " + opsDefineDict_[_key])
                sys.exit(1)
        else:
            _opsKeyValueDict[_key] = _opsDict.__dict__[_key]

    return _opsKeyValueDict


if __name__ == "__main__":
    # doStrAsCmd("PWD", "/Users/nobody/Documents/develop/", True)

    # removeMacXattr("/Volumes/Files/develop/GitHub/PY_Service/Excel/res/services/File/MoveFiles/MoveFiles.xlsx")

    # _fileList = folderUtils.getFileListInFolder("/Users/nobody/Downloads/unity-asset-checker-mac-1.16.8", [".dll"])

    # _fileList = folderUtils.getFilterFilesInPath(
    #     "/disk/XS/native-master-pj/output/for_unity/OSX/")
    # for _i in range(len(_fileList)):
    #     removeMacXattr(_fileList[_i])

    killCmd("tsc --watch --project tsconfig.json")
