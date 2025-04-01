from utils.dotUtil.DotNode import DotNode


class DotNodeRelation:
    def __init__(self, label_: str, fromNode_: DotNode, toNode_: DotNode):
        self.label = label_
        self.fromNode: DotNode = fromNode_
        self.toNode: DotNode = toNode_

    def toDotContent(self):
        return f'{self.fromNode.name} -> {self.toNode.name} [label = {self.label}]'


if __name__ == "__main__":
    _infoRoot = DotNodeRelation()
