#!/usr/bin/env python3
# Created by nobody at 2023/12/22
from base.supports.Base.BaseInService import BaseInService
from utils import folderUtils
from utils import sysUtils
from utils import cmdUtils
from utils import printUtils
from utils import fileUtils
from utils import pyServiceUtils
import os
import shutil

'''
puml-gen puml文件的生成工具 (https://github.com/pierre3/PlantUmlClassDiagramGenerator)
    puml-gen /Volumes/scriptFolder/ /Volumes/pumlFolder/ -dir
plantuml 工具 (http://plantuml.com/download)
    java -jar /Volumes/plantuml.jar -tsvg /Volumes/pumlFolder/puml.puml
'''


class CSharpUML(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.csFolderPath: str = None
        self.pUmlFolderPath: str = None
        self.umlFolderPath: str = None

    def create(self):
        super(CSharpUML, self).create()

    def destroy(self):
        super(CSharpUML, self).destroy()

    def createPuml(self):
        # 生成 puml 文本文件，cs文件和puml文件一一对应
        _umlDocCMD = "/users/nobody/.dotnet/tools/puml-gen " + self.csFolderPath + " " + self.pUmlFolderPath + " -dir"
        cmdUtils.doStrAsCmd(_umlDocCMD, self.pUmlFolderPath, True)
        # puml-gen 会生成一个 include.puml 文件，用来整合所有的文件
        _pUmlList = folderUtils.getFileListInFolder(self.pUmlFolderPath, [".puml"])
        # include.puml 的内容格式和最新的plantuml不匹配，我们手动生成一个
        _includeContent = "@startuml\n"
        # 先打印最外层文件
        for _i in range(len(_pUmlList)):
            _includeContent += "!include " + _pUmlList[_i] + "\n"
        _includeContent += "@enduml"
        # 覆盖掉原有的 include.puml
        fileUtils.writeFileWithStr(os.path.join(self.pUmlFolderPath, "include.puml"), _includeContent)

    def createUML(self, pUmlPath_: str):
        # 判断其存在性
        if not os.path.exists(pUmlPath_):
            printUtils.pError("ERROR : puml文件错误")
        # 获取 puml 所在文件夹
        _pUmlFolderPath = os.path.dirname(pUmlPath_)
        _justName = os.path.splitext(os.path.split(pUmlPath_)[1])[0]
        # 通过 puml  生成 uml 图
        _umlPicCMD = "java -jar " + self.plantUMLJar + " -tsvg " + pUmlPath_
        cmdUtils.doStrAsCmd(_umlPicCMD, _pUmlFolderPath, True)
        # 将生成的 puml 转移到指定文件夹内
        _umpPath = os.path.join(_pUmlFolderPath, _justName + ".svg")
        if os.path.exists(_umpPath):
            shutil.copy(_umpPath, os.path.join(self.umlFolderPath, _justName + ".svg"))
            os.remove(pUmlPath_)
            os.remove(_umpPath)
        else:
            printUtils.pError("ERROR : UML图创建错误")

    # 为每一个目录创建一个UML图
    def createIncludePUml(self):
        # 获得文件夹列表
        _pumlFolderList = folderUtils.getFolderList(self.pUmlFolderPath)
        # 文件夹遍历，获得文件夹和文件夹下文件的关系字典
        _pumlFolderAndFileDict = {}
        for _idx in range(len(_pumlFolderList)):
            _pUmlFolderPath = _pumlFolderList[_idx]
            _pumlFolderAndFileDict[_pUmlFolderPath] = folderUtils.getFileListInFolder(_pUmlFolderPath, [".puml"])
        _includePUmlPathList = []
        # 每一个文件夹生成对应的 puml 文件
        for _pUmlFolderPath in _pumlFolderAndFileDict:
            _pUmlPathList = _pumlFolderAndFileDict[_pUmlFolderPath]
            # 生成文件夹内所包含的puml列表
            _includeContent = "@startuml\n"
            for _idx in range(len(_pUmlPathList)):
                _pUmlPath = _pUmlPathList[_idx]
                _includeContent += "!include " + _pUmlPath + "\n"
            _includeContent += "@enduml"
            _umlName = "include_" + _pUmlFolderPath.split(self.pUmlFolderPath)[1].replace("/", "_")
            # 写入puml文件，文件名和文件夹路径对应
            _includePUmlPath = os.path.join(self.pUmlFolderPath, _umlName + ".puml")
            fileUtils.writeFileWithStr(_includePUmlPath, _includeContent)
            # 记录puml文件路径
            _includePUmlPathList.append(_includePUmlPath)
        # 每个文件夹的 puml  生成对应的 uml
        for _idx in range(len(_includePUmlPathList)):
            _includePUmlPath = _includePUmlPathList[_idx]
            self.createUML(_includePUmlPath)
        return

    def analyseCSharpAndCreateUML(self, csFolderPath_: str, pUmlFolderPath_: str, umlFolderPath_: str, plantUMLJar_: str):
        self.csFolderPath = sysUtils.folderPathFixEnd(csFolderPath_)
        self.pUmlFolderPath = sysUtils.folderPathFixEnd(pUmlFolderPath_)
        self.umlFolderPath = sysUtils.folderPathFixEnd(umlFolderPath_)
        self.plantUMLJar = plantUMLJar_

        # 如果存在已经生成的puml文件，删除掉。
        if os.path.exists(self.pUmlFolderPath):
            folderUtils.removeTree(self.pUmlFolderPath)
        folderUtils.makeSureDirIsExists(self.pUmlFolderPath)
        folderUtils.makeSureDirIsExists(self.umlFolderPath)

        # 打印文件结构
        folderUtils.showFileStructureReg(self.csFolderPath, [".*\.cs$"])

        self.createPuml()  # 将 cs 解析生成 puml
        # 使用 puml 的 include.puml 生成 uml 图。
        self.createUML(os.path.join(self.pUmlFolderPath, "include.puml"))
        # 为每一个文件夹生成相应的 uml 图
        self.createIncludePUml()


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr: CSharpUML = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    # _nameSpace = "XS"  # 命名空间
    # _csFolderPath = "/disk/XS/SLG/DEV/projects/cs/project_unity/Assets/Scripts/"  # 代码的位置

    _nameSpace = "CS_Service"  # 命名空间
    _csFolderPath = "/Users/nobody/Documents/develop/GitHub/Services/CS_Service/"  # 代码的位置

    _pUmlFolderPath = os.path.join(_subSvr.subResPath, _nameSpace, "PUML")  # 生成puml文件的位置
    _umlFolderPath = os.path.join(_subSvr.subResPath, _nameSpace, "UMLPIC")  # 将 puml 转换成 UML 图的位置
    _plantUmlJar = os.path.join(_subSvr.subResPath, "support", "plantuml.jar")  # 工具路径
    # _cmd = f'java -jar {_plantUmlJar} -testdot'
    # print('_cmd = ' + str(_cmd))
    # _lines = cmdUtils.doStrAsCmdAndGetPipeline(_cmd, os.path.join(_svr.resPath, _nameSpace))
    # for _i in range(len(_lines)):
    #     print(str(_lines[_i]))
    # sys.exit(1)
    _subSvr.analyseCSharpAndCreateUML(_csFolderPath, _pUmlFolderPath, _umlFolderPath, _plantUmlJar)  # CS -> 结构 -> UML
