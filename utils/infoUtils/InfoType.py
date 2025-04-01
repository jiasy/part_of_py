from enum import Enum


class InfoType(Enum):
    NONE = 0
    ExcelShape = 1  # 在同一个 Sheet 中 shape 多了就会慢
    ExcelCell = 2
    Color = 3
