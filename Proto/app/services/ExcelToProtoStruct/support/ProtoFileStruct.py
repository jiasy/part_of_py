from utils.excelDataUtils import DataCol
from Proto.app.services.ExcelToProtoStruct.support.ProtoFileField import ProtoFileField


class ProtoFileStruct:
    def __init__(self, rootName_: str, name_: str):
        self.rootName = rootName_
        self.name = name_
        self.protoFieldList: list[ProtoFileField] = []

    #删
