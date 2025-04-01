# !/usr/bin/env python3

import re
from git import Repo  # 导入repo模块
import os
import json
import getopt
import sys
import functools
import ftplib
import stat
import shutil
from pathlib import Path, PureWindowsPath
import platform
import zipfile
import base64
from utils import folderUtils

fileUpdatedCount = 0
fileNeedToUpdate = 0


class FTPSync(object):
    def __init__(self, host_: str, username_: str, password_: str, ftpFolder_: str = None):
        self.ftpConnect = ftplib.FTP(host_, username_, password_)  # host, user, passwd
        self.ftpFolder = ""
        if ftpFolder_:
            # 去掉文件路径后面的 /
            if ftpFolder_[-1] == "/":
                ftpFolder_ = ftpFolder_[:-1]
            self.ftpFolder = ftpFolder_
            self.ftpConnect.cwd(self.ftpFolder)  # 远端FTP目录

    def get_dirs_files(self):
        u''' 得到当前目录和文件, 放入dir_res列表 '''
        dir_res = []
        self.ftpConnect.dir('.', dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return files, dirs

    # 遍历文件夹
    # ftpUtils.walk('.')
    def walk(self, next_dir, resultList_: list = None):
        # 文件列表
        _resultList = resultList_ if resultList_ else []
        # ftp 端切换到文件夹
        self.ftpConnect.cwd(next_dir)
        # ftp 端的文件夹
        ftp_curr_dir = self.ftpConnect.pwd()
        ftp_relative_curr_dir = ftp_curr_dir.split(self.ftpFolder)[1]
        # ftp 当前指向目录下的文件
        files, dirs = self.get_dirs_files()
        # ftp 端的文件相对路径
        for _file in files:
            _filePath = ftp_relative_curr_dir + "/" + _file
            _resultList.append(_filePath)
            print('_filePath = ' + str(_filePath))
        # 遍历文件夹
        for d in dirs:
            self.ftpConnect.cwd(ftp_curr_dir)  # 切换ftp的当前工作目录为d的父文件夹
            self.walk(d, _resultList)  # 在这个递归里面，本地和ftp的当前工作目录都会被更改
        # 返回结果集
        return _resultList

    # ftp.syncToLocal('.')
    def syncToLocal(self, next_dir):
        # ftp 端切换到文件夹
        self.ftpConnect.cwd(next_dir)
        # 本地创建相同的目录
        try:
            os.mkdir(next_dir)
        except OSError:
            pass
        os.chdir(next_dir)
        # ftp 端的文件夹
        ftp_curr_dir = self.ftpConnect.pwd()
        # 本机的文件夹
        local_curr_dir = os.getcwd()
        # ftp 当前指向目录下的文件
        files, dirs = self.get_dirs_files()
        # 遍历文件
        for f in files:
            print('download :', os.path.abspath(f))
            outf = open(f, 'wb')
            try:
                self.ftpConnect.retrbinary('RETR %s' % f, outf.write)
            finally:
                outf.close()
        # 遍历文件夹
        for d in dirs:
            os.chdir(local_curr_dir)  # 切换本地的当前工作目录为d的父文件夹
            self.ftpConnect.cwd(ftp_curr_dir)  # 切换ftp的当前工作目录为d的父文件夹
            self.syncToLocal(d)  # 在这个递归里面，本地和ftp的当前工作目录都会被更改


def uploadFolder(ftpSync_, localFolderPath_, ftpFolderPath_=None):
    print("%s" % (localFolderPath_))
    _ftpConnect = ftpSync_.ftpConnect
    _fileList = os.listdir(localFolderPath_)

    # 先记住之前在哪个工作目录中
    _lastFolder = os.path.abspath('.')
    # 然后切换到目标工作目录
    os.chdir(localFolderPath_)

    if ftpFolderPath_:
        _currentTargetFolderPath = _ftpConnect.pwd()
        try:
            _ftpConnect.mkd(ftpFolderPath_)
        except Exception:
            pass
        finally:
            _ftpConnect.cwd(os.path.join(_currentTargetFolderPath, ftpFolderPath_))

    for _fileName in _fileList:
        _currentTargetFolderPath = _ftpConnect.pwd()
        _currentLocal = localFolderPath_ + r'/{}'.format(_fileName)
        if os.path.isfile(_currentLocal):
            uploadFile(ftpSync_, localFolderPath_, _fileName)
        elif os.path.isdir(_currentLocal):
            _currentTargetFolderPath = _ftpConnect.pwd()
            try:
                _ftpConnect.mkd(_fileName)
            except:
                pass
            _ftpConnect.cwd("%s/%s" % (_currentTargetFolderPath, _fileName))
            uploadFolder(ftpSync_, _currentLocal)

        # 之前路径可能已经变更，需要再回复到之前的路径里
        _ftpConnect.cwd(_currentTargetFolderPath)

    os.chdir(_lastFolder)


def uploadFile(ftpSync_, localFolderPath_, fileName_, ftpFolderPath_=None, callback_=None):
    global fileUpdatedCount
    _ftpConnect = ftpSync_.ftpConnect
    # 记录当前 ftp 路径
    _currentFolder = _ftpConnect.pwd()

    if ftpFolderPath_:
        try:
            _ftpConnect.mkd(ftpFolderPath_)
        except:
            pass
        finally:
            _ftpConnect.cwd(os.path.join(_currentFolder, ftpFolderPath_))

    file = open(os.path.join(localFolderPath_, fileName_), 'rb')  # file to send
    _ftpConnect.storbinary('STOR %s' % fileName_, file, callback=callback_)  # send the file
    file.close()  # close file
    fileUpdatedCount = fileUpdatedCount + 1
    print(
        "    %s/%s %s / %s" % (
            str(fileUpdatedCount),
            str(fileNeedToUpdate),
            localFolderPath_,
            fileName_
        )
    )
    _ftpConnect.cwd(_currentFolder)


# 写文件
def writeFileWithStr(filePath_: str, str_: str):
    if not os.path.exists(os.path.dirname(filePath_)):
        os.makedirs(os.path.dirname(filePath_))
    try:
        _file = open(filePath_, 'w')
        try:
            _file.write(str_)
        finally:
            _file.close()
    except Exception as e:
        print(filePath_, e)


# json文件直接读取成字典
def dictFromJsonFile(jsonPath_: str):
    return json.loads(readFromFile(jsonPath_))


def readFromFile(filePath_: str):
    _contentStr = None
    try:
        _file = open(filePath_, 'r')
        try:
            _contentStr = _file.read()
        finally:
            _file.close()
    except Exception as e:
        print(filePath_, e)
    return _contentStr


def versionCompare(v1: str = "1.1.1", v2: str = "1.2"):
    if not isVersionStr(v1) or not isVersionStr(v2):
        return None
    v1_list = v1.split(".")
    v2_list = v2.split(".")
    v1_len = len(v1_list)
    v2_len = len(v2_list)
    if v1_len > v2_len:
        for i in range(v1_len - v2_len):
            v2_list.append("0")
    elif v2_len > v1_len:
        for i in range(v2_len - v1_len):
            v1_list.append("0")
    else:
        pass
    for i in range(len(v1_list)):
        if int(v1_list[i]) > int(v2_list[i]):
            # v1大
            return 1
        if int(v1_list[i]) < int(v2_list[i]):
            # v2大
            return -1
    # 相等
    return 0


# 检测当前名称是否是版本号 x.x.x
def isVersionStr(ver_: str):
    _verCheck = re.match("\d+(\.\d+){0,2}", ver_)
    if _verCheck is None or _verCheck.group() != ver_:
        return False
    else:
        return True


# 获取编译语句
def getBuildCmd(cocosCreatorAppPath_, projectFolder_: str, configJsonPath_: str):
    _cmd = cocosCreatorAppPath_ + \
           " --path " + projectFolder_ + \
           " --build \"configPath=" + configJsonPath_ + "\""
    return _cmd


# 修改 game.json 的超时时间设置
def changeGameJson(buildFolderPath_: str):
    _gameJsonPath = str(Path(buildFolderPath_ + "/wechatgame/game.json"))
    _gameJsonDict = dictFromJsonFile(_gameJsonPath)
    _gameJsonDict["networkTimeout"]["request"] = 60000
    _gameJsonDict["networkTimeout"]["connectSocket"] = 60000
    _gameJsonDict["networkTimeout"]["uploadFile"] = 60000
    _gameJsonDict["networkTimeout"]["downloadFile"] = 60000
    _jsonStr = str(json.dumps(_gameJsonDict, indent=4, sort_keys=False, ensure_ascii=False))
    writeFileWithStr(_gameJsonPath, _jsonStr)


# 修改 appConfig.json
def changeAppConfigJson(appConfigPath_: str, currentVer_: str, isTest_: bool):
    _appConfigDict = dictFromJsonFile(appConfigPath_)
    _appConfigDict["version"] = currentVer_
    if isTest_:
        # QA测试
        _appConfigDict["networkInfo"]["audit"] = "ws://ip:port"
        _appConfigDict["networkInfo"]["release"] = _appConfigDict["networkInfo"]["audit"]
    else:
        # 提审或者正式
        _appConfigDict["networkInfo"]["audit"] = "wss://网址"
        _appConfigDict["networkInfo"]["release"] = "wss://网址"
    _jsonStr = str(json.dumps(_appConfigDict, indent=4, sort_keys=False, ensure_ascii=False))
    writeFileWithStr(appConfigPath_, _jsonStr)


# 修改 WeChatGameConfig.json
# 修改其中的构建目录，指向当前build
def changeWeChatGameConfigJson(weChatGameConfigJsonPath_: str, buildPath_: str, isTest_: bool, ver_: str):
    _weChatGameConfigDict = dictFromJsonFile(weChatGameConfigJsonPath_)
    _weChatGameConfigDict["buildPath"] = buildPath_
    if isTest_:
        # QA测试
        _weChatGameConfigDict["wechatgame"][
            "REMOTE_SERVER_ROOT"] = "https://网址/QA_Test/" + ver_ + "/"
    else:
        # 提审或者正式
        _weChatGameConfigDict["wechatgame"][
            "REMOTE_SERVER_ROOT"] = "https://网址/wsg/" + ver_ + "/"
    _jsonStr = str(json.dumps(_weChatGameConfigDict, indent=4, sort_keys=False, ensure_ascii=False))
    writeFileWithStr(weChatGameConfigJsonPath_, _jsonStr)


def printList(list_: list, prefix_: str = ""):
    _length: int = len(list_)
    for _idx in range(_length):
        print(prefix_ + str(_idx) + ' : ' + str(str(list_[_idx])))


def os_is_mac():
    return platform.system() == "Darwin"


# 0 脚本文件在工程目录下
# 1 ssh登陆Git
# 2 确保当前目录都push到远程
# 3 可以填写 -v 作为版本指定，也可不填写，会默认在当前最大版本上加 0.0.1
# 4 WeChatGameConfig.json 填写构建参数，也就是构建的目标路径，使用的远程资源地址
# 5 assets/resources/configs/AppConfig.json 内为 wss 地址，当前版本号
# 6 流程如下
#      链接Git 获取tag信息，并创建一个新tag，确保它最大。
#      修改本地的appConfig
#      构建工程，并记录res下的文件个数
#      修改构建目录下的game.json，确保延时加载的时间为 6000 毫秒
#      将 res 目录上传至 ftp，
#      将 res 打包成 zip
#      成功后删除 本地 res
#      结束流程，之后就是手工的打开 微信开发者工具，手动上传即可。
# python3 CocosCreatorBuild.py -v 1.1.1
if __name__ == "__main__":
    # 删