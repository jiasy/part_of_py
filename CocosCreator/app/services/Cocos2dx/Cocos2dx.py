#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import folderUtils
import os
import sys


class Cocos2dx(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(Cocos2dx, self).create()

    def destroy(self):
        super(Cocos2dx, self).destroy()


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)

    # ios 工程编译命令
    _fguiProjectFolderPath = "/Users/nobody/Documents/develop/GitHub/FGUI/FairyGUI-cocos2dx"
    _ios_build_folder = os.path.join(_fguiProjectFolderPath, "Examples", "ios_build")
    folderUtils.makeSureDirIsExists(_ios_build_folder)
    _compileIosProjectCmd = f"cd {_ios_build_folder};cmake .. -GXcode -DCMAKE_SYSTEM_NAME=iOS"
    print('_compileIosProjectCmd = \n' + str(_compileIosProjectCmd))

    sys.exit(1)

    # Cocos2dx-4 引擎代码
    _cocos2dx_source_folder_path = "/Users/nobody/Documents/develop/GitRepository/cocosCreator/cocos2d-x-4"
    # 命令行工具 下载到 tools/cocos2d-console 中
    _cocos2dx_tools_console_path = os.path.join(_cocos2dx_source_folder_path, "tools/cocos2d-console/bin/")
    _cocos2dx_tools_console = os.path.join(_cocos2dx_tools_console_path, "cocos.py")

    # 目标工程
    _projectName = "cocos2dx_ios_mac"
    # 包名
    _projectPkg = "com.cocos2dx.ios_mac"
    # 工程文件夹
    _projectFolderPath = "/Users/nobody/Documents/develop/selfDevelop/CocosCreator/Cocos4/"
    # 确保工程文件夹存在
    folderUtils.makeSureDirIsExists(_projectFolderPath)

    # 切 Python2 环境，因为 cocos2dx 的命令行工具只支持 2.7
    _switchToPython2Cmd = f"source activate py2"
    # cocos 命令行创建工程
    _createProjectCmd = f"python2 {_cocos2dx_tools_console}"
    _createProjectCmd = _createProjectCmd + f" new {_projectName}"
    _createProjectCmd = _createProjectCmd + f" -p {_projectPkg}"
    _createProjectCmd = _createProjectCmd + f" -d {_projectFolderPath}"  # 在这里创建 _projectName 文件夹
    _createProjectCmd = _createProjectCmd + f" -l cpp"
    # ;分割在一个命令里执行，以免分两次执行，第二个又将python环境回复到3
    _createCocosProjectCmd = f"{_switchToPython2Cmd};{_createProjectCmd}"
    print('_createCocosProjectCmd = \n' + str(_createCocosProjectCmd))

    # ios 工程编译命令
    _ios_build_folder = os.path.join(_projectFolderPath, _projectName, "ios_build")
    folderUtils.makeSureDirIsExists(_ios_build_folder)
    _compileIosProjectCmd = f"cd {_ios_build_folder};cmake .. -GXcode -DCMAKE_SYSTEM_NAME=iOS"
    print('_compileIosProjectCmd = \n' + str(_compileIosProjectCmd))
