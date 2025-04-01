#!/usr/bin/env
import sys

sys.path.append("/Users/nobody/Documents/develop/GitHub/Services/PY_Service")

from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
import http.server
import ssl
import os
from utils import cmdUtils
from utils import folderUtils
from utils import sysUtils
from optparse import OptionParser


# 通过 命令行 创建一个文件
def doCmdCreateFile(cmd_: str, whichFolder_: str, filePath_: str, inputData_: str = None):
    if not os.path.exists(filePath_):
        cmdUtils.doStrAsCmd(cmd_, whichFolder_, False, inputData_)
    if not os.path.exists(filePath_):
        print(f"ERROR : {filePath_}")
        return False
    else:
        print(f"Success ： {filePath_}")
        return True


class SLL_Server(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(SLL_Server, self).create()

    def destroy(self):
        super(SLL_Server, self).destroy()

    # 获取自签名文件
    def get_self_signed_certificate(self, pemContainerFolder_: str):
        folderUtils.makeSureDirIsExists(pemContainerFolder_)
        _keyPath = os.path.join(pemContainerFolder_, 'key.pem')
        _csrPath = os.path.join(pemContainerFolder_, 'csr.csr')
        _certPath = os.path.join(pemContainerFolder_, 'cert.pem')
        # 命令会生成一个文件时，如何打印和校验
        sys.exit(1) if not doCmdCreateFile(f'openssl genrsa -out {_keyPath} 2048', pemContainerFolder_, _keyPath) else None
        _inputDataStr = "\n".join([
            "CN",  # Common Name
            "StateOrProvince",
            "LocalityName",
            "OrganizationName",
            "OrganizationalUnitName",
            "CommonName",
            "EmailAddress",
            "password",
            "optional company name",
        ]) + "\n"
        sys.exit(1) if not doCmdCreateFile(f'openssl req -new -sha256 -key key.pem -out {_csrPath}', pemContainerFolder_, _csrPath, _inputDataStr) else None
        sys.exit(1) if not doCmdCreateFile(f'openssl x509 -req -sha256 -days 365 -in {_csrPath} -signkey {_keyPath} -out {_certPath}', pemContainerFolder_, _certPath) else None
        return _keyPath, _csrPath, _certPath

    # 启动服务并等待
    def startServerWaitForever(self, nameSpace_: int, port_: int, serverFolder_: str = None):
        if sysUtils.is_port_in_use(port_):
            print(f"ERROR : {port_} is in use")
            sys.exit(1)
        # 没指定的话，使用 resPath 中的相应目录
        if serverFolder_ is None:
            serverFolder_ = os.path.join(self.resPath, nameSpace_)

        # SLL相关文件路径
        _keyCsrCertFolder = os.path.join(self.resPath, nameSpace_, "key_csr_cert")
        _keyPath, _csrPath, _certPath = self.get_self_signed_certificate(_keyCsrCertFolder)
        # 切换路径
        os.chdir(serverFolder_)  # 切换到指定目录，在这里启动服务器
        # 确认当前工作目录是否已切换到指定目录
        if os.getcwd() == serverFolder_:
            print(f"Server successfully started on : {serverFolder_}")
        else:
            print(f"ERROR : fail chdir")
            sys.exit()

        # 启动服务
        _server_address = ('localhost', port_)
        _httpd = http.server.HTTPServer(_server_address, http.server.SimpleHTTPRequestHandler)
        _httpd.socket = ssl.wrap_socket(_httpd.socket, certfile=_certPath, keyfile=_keyPath, server_side=True)
        _httpd.serve_forever()


'''
    /Users/nobody/anaconda3/envs/py_3_10/bin/python /Users/nobody/Documents/develop/GitHub/Services/PY_Service/Server/app/services/SLL_Server/SLL_Server.py --nameSpace UnityWebGL --unityWebGlBuildPath $(pwd)
'''
if __name__ == '__main__':
    _svr: SLL_Server = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)

    _opsDefineDict: dict = {}
    _opsDefineDict["nameSpace"] = '命名空间'
    _opsDefineDict["unityWebGlBuildPath"] = 'Unity构建出的目录'

    # 参数合并构建
    _opsDict = cmdUtils.getOps(_opsDefineDict, OptionParser())

    _nameSpace = _opsDict["nameSpace"]
    _unityWebGlBuildPath = _opsDict["unityWebGlBuildPath"]

    # 判断命令行执行位置
    if os.getcwd() != _unityWebGlBuildPath:
        print(f"ERROR : 执行目录必须和参数一致 \n    {os.getcwd()}\n    {_unityWebGlBuildPath}")
        sys.exit(1)

    _svr.startServerWaitForever("UnityWebGL", 8000, _unityWebGlBuildPath)
