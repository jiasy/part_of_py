import sys

from utils.excelDataUtils import DataCol
from utils.excelDataUtils import DataType


class ProtoFileField:
    def __init__(self, rootName_: str, id_: int, dataCol_: DataCol):
        self.rootName = rootName_
        self.id = id_
        self.dataCol = dataCol_
    # 删
