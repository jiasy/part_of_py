#!/usr/bin/env python3
# Created by nobody at 2023/12/22
import os.path

from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import folderUtils
from utils import fileUtils
from utils import sysUtils
from utils import cmdUtils


# js 的引用关系图
class JavaScriptRequireDot(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(JavaScriptRequireDot, self).create()

    def destroy(self):
        super(JavaScriptRequireDot, self).destroy()

    # 检测并尝试安装
    def checkThenInstallMadge(self):
        sysUtils.npmCheckThenInstall("madge")

    # 生成指定文件的 require 图
    def createRelationDot(self, nameSpace_: str, jsPath_: str):
        _resPath = os.path.join(self.subResPath, nameSpace_)
        folderUtils.makeSureDirIsExists(_resPath)
        _jsJusName = fileUtils.justName(jsPath_)
        _gvPath = os.path.join(_resPath, f'{_jsJusName}.gv')
        _cmdStr = f"cd {_resPath};"
        _cmdStr = f"{_cmdStr}madge --dot {jsPath_} > {_gvPath};"
        _cmdStr = f"{_cmdStr}dot -Tsvg {_jsJusName}.gv -o {_jsJusName}.svg"
        # python 下运行 npm 命令，npm 再执行 环境中的 dot 有权限问题
        # 这里不解决，打印出命令手动贴一下回车
        # cmdUtils.doStrAsCmd(_cmdStr, _resPath)
        return _cmdStr


if __name__ == '__main__':
    _subSvr_JavaScriptRequireDot: JavaScriptRequireDot = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr_JavaScriptRequireDot.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    from utils.CompanyUtil import Company_BB_Utils

    # 查看指定 js 的引用，这个图非常大。。。引用的引用也会显示出来。。。
    _targetJsPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts/dist/Game/Module/Battle/BattleEngine/Client/BattleView.js")
    _cmdStr = _subSvr_JavaScriptRequireDot.createRelationDot("XS", _targetJsPath)
    print(_cmdStr)
