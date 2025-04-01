class ConfigSheet:
    def __init__(self, excelName_: str, sheetName_: str):
        self.RowIdFromPy = -1  # py读取数据时记录的行号
        self.Id = None  # Id
        self.excelName = excelName_  # 所在 excel 名称
        self.sheetName = sheetName_  # 代表哪个 sheet 的数据格式

    def init(self, cfg_):
        self.Id = cfg_["Id"]
        self.RowIdFromPy = cfg_["RowIdFromPy"]

    def toDict(self):
        return {"Id": self.Id, "RowIdFromPy": self.RowIdFromPy}
