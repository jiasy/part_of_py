#!/usr/bin/env python3
# Created by nobody at 2023/12/25
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import fileUtils
from utils import folderUtils
from utils import fileCopyUtils
import os


class CSharpClassRelation(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(CSharpClassRelation, self).create()

    def destroy(self):
        super(CSharpClassRelation, self).destroy()

    # 拷贝指定文件夹的代码
    def copyCode(self, srcCSharpFolder_: str, nameSpace_: str):
        _tarCSharpFolder = os.path.join(self.subResPath, "Code", nameSpace_)
        folderUtils.deleteThenCreateFolder(_tarCSharpFolder)  # 确保其内容为新
        fileCopyUtils.copyFilesInDir(srcCSharpFolder_, _tarCSharpFolder, False, [".cs"])  # 将脚本拷贝过来，保持其结构
        folderUtils.showFileStructureReg(_tarCSharpFolder, [".*\.cs$"], True)  # 打印拷贝过来的代码结构
        return _tarCSharpFolder

    # 加工代码，并解析，之后生成图
    def drawClassRelationInDot(self, srcCSharpFolder_: str, passSubFolder_: str, nameSpace_: str):
        _tarCSharpFolder = self.copyCode(srcCSharpFolder_, nameSpace_)  # 拷贝并返回拷贝的副本文件夹
        from Unity.app.services.UnityCSharpAnalyse import UnityCSharpAnalyse
        _svr_UnityCSharpAnalyse: UnityCSharpAnalyse = pyServiceUtils.getSvrByName("Unity", "UnityCSharpAnalyse")
        _svr_UnityCSharpAnalyse.drawClassRelationInDot(_tarCSharpFolder, passSubFolder_)
        folderUtils.removeTree(_tarCSharpFolder)  # 删除拷贝的代码


if __name__ == '__main__':
    _subSvr_CSharpClassRelation: CSharpClassRelation = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr_CSharpClassRelation.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    from utils.CompanyUtil import Company_BB_Utils

    _nameSpace = "Scripts"
    _unityCSharpFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_unity", "Assets", "Scripts")
    _subSvr_CSharpClassRelation.drawClassRelationInDot(
        _unityCSharpFolder, [
            "AddonExtend/Puerts"
        ],
        _nameSpace
    )
