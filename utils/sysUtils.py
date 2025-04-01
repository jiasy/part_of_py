# !/usr/bin/env python3
import os
import sys
import platform
from utils import fileUtils
from utils import cmdUtils
import subprocess
from utils import printUtils
from utils import strUtils
import socket
import psutil
import utils.printUtils


def dotnetCheckThenInstall(packageName_):
    checkThenInstall(
        ['dotnet', 'tool', 'list', '--global'],  # 列当前持有包
        ['dotnet', 'tool', 'install', '-g', packageName_]  # 安装
    )


def npmCheckThenInstall(packageName_):
    checkThenInstall(
        ['npm', 'list', '-g', packageName_],  # 列当前持有包
        ['npm', 'install', '-g', packageName_]  # 安装
    )


def brewCheckThenInstall(packageName_: str):
    checkThenInstall(
        ['brew', 'list'],  # 列当前持有包
        ['brew', 'install', packageName_]  # 安装
    )


def checkThenInstall(checkCmdList_: list[str], installCmdList_: list[str]):
    _envKey = checkCmdList_[0]
    _packageName = installCmdList_[-1]
    if _envKey != installCmdList_[0]:
        utils.printUtils.pError("ERROR : 环境不一致")
    _isInstalled = False
    try:
        _installedPackages = subprocess.check_output(checkCmdList_, text=True)
        _isInstalled = _packageName in _installedPackages  # 检查输出中是否包含 'prettier'
    except subprocess.CalledProcessError as e:
        _isInstalled = False
    # 没装
    if not _isInstalled:
        try:
            subprocess.check_call(installCmdList_)
            print(f"{_envKey} - {_packageName} 安装成功")
        except subprocess.CalledProcessError as e:
            # 处理安装失败的情况
            print(f"ERROR : {_envKey} - {_packageName} 安装失败: {e}")
    else:
        print(f"{_envKey} - {_packageName} 已安装")


# -------------------------------- 进程、端口 --------------------------------------------------------------------------------
def is_process_running(programName_: str) -> bool:
    for _process in psutil.process_iter(['name']):
        if _process.info['name'] == programName_:
            return True
    return False


def is_port_in_use(port_):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port_))
        except OSError:
            return True
        return False


# 通过端口号杀进程
def kill_related_processes_by_port(port_):
    for _proc in psutil.process_iter(['pid', 'name']):
        try:
            _connections = _proc.connections()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

        for _conn in _connections:
            if _conn.laddr.port == port_ and _proc.pid != os.getpid():
                try:
                    _proc.kill()
                    print(f"Process with PID {_proc.pid} using port {port_} has been terminated.")
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    print(f"Failed to terminate process with PID {_proc.pid} using port {port_}.")


# ------------------------------------系统判断----------------------------------------------------------------------------------
def os_is_win32():
    return sys.platform == 'win32'


def os_is_32bit_windows():
    if not os_is_win32():
        return False
    arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
    archw = "PROCESSOR_ARCHITEW6432" in os.environ
    return arch == "x86" and not archw


def os_is_windows():
    return platform.system() == "Windows"


def os_is_mac():
    return platform.system() == "Darwin"


def os_is_linux():
    return platform.system() == "Linux"


def pathJoin(pathPrefix_: str, pathSuffix_: str):
    if pathSuffix_.startswith(os.path.sep):
        pathSuffix_ = pathSuffix_[1:]
    return os.path.join(pathPrefix_, pathSuffix_)


# 文件夹 路径 修改
def folderPathFixEnd(path_str):
    # 删


# 获取剪切板
def getClipboardData():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    _ = p.wait()
    data = p.stdout.read()
    # 这里的data为bytes类型，之后需要转成utf-8操作
    return str(data, 'utf-8')


# 设置剪切板
def setClipboardData(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    p.communicate()


# 从剪切板中获取图片路径列表
def getClipBoardPathList(upperFilterList_: str):
    _clipPathListStr = getClipboardData()
    _clipPathList = _clipPathListStr.split('\n')
    if len(_clipPathList) == 0:
        return None
    for _i in range(len(_clipPathList)):
        _filePath = _clipPathList[_i]
        if '/' not in _filePath:
            print("剪切板内容不是路径 : \n" + _filePath)
            return None
        _suffixUpper = fileUtils.getUpperSuffix(_filePath)  # 取大写后缀
        if _suffixUpper not in upperFilterList_:  # 判断后缀是否在给定范围内
            print(_filePath + " 后缀 " + _suffixUpper + " 不在 " + str(upperFilterList_) + " 中")
            return None
    # 返回文件路径列表（每一行都是符合条件的路径）
    return _clipPathList


# 文件变更执行权限
# sysUtils.chmod("777","路径",["com.apple.quarantine"],True)
def chmod(type_: str, filePath_: str, deleteUrlList_: list, printPipeLines_: bool = False):
    if os_is_mac():  # mac多了一步
        for _i in range(len(deleteUrlList_)):
            cmdUtils.doStrAsCmd(
                "xattr -dr '" + deleteUrlList_[_i] + "' '" + os.path.basename(filePath_) + "'",  # mac系统下去掉 @ 权限
                os.path.dirname(filePath_),  # 文件所在的文件夹内执行
                printPipeLines_  # 打印命令pipeline
            )
    # 1 可执行 --x
    # 2 可写 -w-
    # 3 可写执行 -wx
    # 4 可读 r--
    # 5 可读执行 r-x
    # 6 可读写 rw-
    # 7 可读写执行 rwx
    if type_ == "111" or type_ == "222" or type_ == "444" or type_ == "666" or type_ == "777" or type_ == "333" or type_ == "555":
        cmdUtils.doStrAsCmd(
            "chmod -R " + type_ + " '" + os.path.basename(filePath_) + "'",  # 可读可写不可执行 666
            os.path.dirname(filePath_),
            printPipeLines_
        )
    else:
        print(f"ERROR : {type_} 不支持")
        sys.exit(1)


# 关闭 上一个 简易服务器
def closeLastSimpleSever(command_: str, port_):
    _pipLineList = cmdUtils.doCmdAndGetPiplineList("lsof", "-i", "tcp:{}".format(port_))
    printUtils.printList(_pipLineList)

    for _i in range(len(_pipLineList)):
        _line = _pipLineList[_i]
        if _line.contains(":{}".format(port_)):
            _line = strUtils.spacesReplaceToSpace(_line)  # 多Space 变 单 Space
            _command = _line.split(" ")[0]
            _pid = _line.split(" ")[1]
            if _command == command_:  # 是 COMMAD 和 Port 全对的上，就算找到了
                cmdUtils.doCmdAndGetPiplineList("kill", "-9", _pid)


# 简易 服务器
# 在 终端中 ，CD 到目录，执行 'python -m http.server 8581' 在所在文件夹创建服务
def simpleSever(port_):
    print(f"python -m http.server {port_}")
    # # closeLastSimpleSever("python3.7",port_)
    # with socketserver.TCPServer(("", port_), http.server.SimpleHTTPRequestHandler) as httpd:
    #     print("serving at port", port_)
    #     httpd.serve_forever()


# 打印环境变量
def showEnv():
    _envDict = dict(os.environ)
    _sortedKeys = sorted(_envDict.keys())
    for _key in _sortedKeys:
        _value = _envDict[_key]
        if _key != "PATH":
            print(f'{_key} = {_value}')
        else:
            print(f'{_key} =')
            _pathList = _value.split(os.pathsep)
            for _path in _pathList:
                print(f'    {_path}')


# ------------------------------------管道出入---------------------------------------------------------------------------------------
# cat filePath | python3.7 py脚本1 脚本参数 | python3.7 py脚本2 脚本参数
# 打开 filePath 文件，内容作为 py脚本1 的输入，py脚本1 操作之后，通过sys.stdout.write(结果)写入输出管道，作为py脚本2的输入
#     # 管道输入
#     sys.stdin
#     # 管道输出
#     sys.stdout
#     # 当前脚本
#     sys.argv[0]
#     # 脚本的第一个参数,以此类推
#     sys.argv[1]

if __name__ == "__main__":
    # simpleSever(8581)
    print(is_process_running("Beyond Compare"))
