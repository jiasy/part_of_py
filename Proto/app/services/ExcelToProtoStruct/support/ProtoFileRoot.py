from Proto.app.services.ExcelToProtoStruct.support.ProtoFileStruct import ProtoFileStruct


class ProtoFileRoot:
    def __init__(self, pkgName_: str, name_: str):
        self.name = name_
        self.pkgName = pkgName_
        self.protoStructList: list[ProtoFileStruct] = []
    # 删