from enum import Enum


class InfoColor(Enum):
    NONE = ""
    Blue = "blue"
    Cyan = "cyan"
    Black = "grey"
    Green = "green"
    Magenta = "magenta"
    Red = "red"
    Grey = "white"
    Yellow = "yellow"

    @staticmethod
    def getColorRgbByType(colorType_):
        if colorType_ is None:
            return 38, 38, 38
        if colorType_ == InfoColor.Blue:
            return 51, 133, 204
        elif colorType_ == InfoColor.Cyan:
            return 0, 152, 152
        elif colorType_ == InfoColor.Black:
            return 0, 0, 0
        elif colorType_ == InfoColor.Green:
            return 73, 141, 54
        elif colorType_ == InfoColor.Magenta:
            return 162, 99, 181
        elif colorType_ == InfoColor.Red:
            return 243, 75, 73
        elif colorType_ == InfoColor.Grey:
            return 117, 117, 117
        elif colorType_ == InfoColor.Yellow:
            return 155, 129, 28
