class DotNode:
    def __init__(self, name_: str):
        self.name = name_

    def toDotContent(self):
        return self.name


if __name__ == "__main__":
    _infoRoot = DotNode("a")
