import sys
from utils.dotUtil.DotNode import DotNode
from utils.dotUtil.DotNodeRelation import DotNodeRelation
import os
from utils import fileUtils
from utils import cmdUtils


class DotRoot:
    def __init__(self, name_: str):
        self.name = name_
        self.nodeList: list[DotNode] = []
        self.nodeRelationList: list[DotNodeRelation] = []

    def getNodeByName(self, nodeName_: str):
        for _i in range(len(self.nodeList)):
            _node = self.nodeList[_i]
            if _node.name == nodeName_:
                return _node
        return None

    def addNodeByName(self, nodeName_: str):
        self.nodeList.append(DotNode(nodeName_))

    def addRelation(self, label_: str, fromNodeName_: str, toNodeName_: str):
        _fromNode = self.getNodeByName(fromNodeName_)
        _toNode = self.getNodeByName(toNodeName_)
        if _fromNode is not None and _toNode is not None:
            self.nodeRelationList.append(DotNodeRelation(label_, _fromNode, _toNode))
        else:
            print(f"ERROR : {fromNodeName_} or {toNodeName_} not found")
            sys.exit(1)

    def stateDotContent(self):
        _stateContent = ""
        for _i in range(len(self.nodeList)):
            _stateContent = f"{_stateContent}{self.nodeList[_i].toDotContent()}\n"
        return _stateContent

    def relationDotContent(self):
        _relationContent = ""
        for _i in range(len(self.nodeRelationList)):
            _relationContent = f"{_relationContent}{self.nodeRelationList[_i].toDotContent()}\n"
        return _relationContent

    def toDotContent(self):
        return f'''
digraph {self.name} {{
{self.stateDotContent()}
{self.relationDotContent()}
}}
        '''

    def toDotPng(self, targetFolder_: str):
        # 生成dot 给 可视化 用
        _targetDotPath = os.path.join(targetFolder_, self.name + ".dot")
        _targetPngPath = os.path.join(targetFolder_, self.name + ".png")
        fileUtils.writeFileWithStr(_targetDotPath, self.toDotContent())
        _graphCmd = "dot '" + _targetDotPath + "' -T png -o '" + _targetPngPath + "'"
        cmdUtils.doStrAsCmd(_graphCmd, targetFolder_, True)


if __name__ == "__main__":
    _infoRoot = DotRoot("Test")
    _infoRoot.addNodeByName("Init")
    _infoRoot.addNodeByName("Login")
    _infoRoot.addNodeByName("Main")
    _infoRoot.addNodeByName("Pop")
    _infoRoot.addNodeByName("Game")
    _infoRoot.addRelation("toLogin", "Init", "Login")
    _infoRoot.addRelation("toMain", "Login", "Main")
    _infoRoot.addRelation("btn_close", "Pop", "Main")
    _infoRoot.addRelation("btn_toMain", "Game", "Main")
    _infoRoot.addRelation("btn_Pop", "Main", "Pop")
    _infoRoot.addRelation("btn_toGame", "Main", "Game")

    _folderPath = os.path.dirname(os.path.realpath(__file__))  # 当前执行目录
    _infoRoot.toDotPng(_folderPath)
