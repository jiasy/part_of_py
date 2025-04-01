

class ConfigLogicRootBase:

    def __init__(cls, subSvr_BBTs_Config_: BBTs_Config, excelFolderPath_: str):
        cls.subSvr_BBTs_Config = subSvr_BBTs_Config_
        cls.excelFolderPath = excelFolderPath_
        # 初始化 - Excel
        cls.excelSwiftTask = None
        cls.excelHero = None
        cls.excelQuickQueue = None
        cls.excelCastleBlock = None
        cls.excelUnitSkill = None
        cls.excelGameAction = None
        cls.excelHelp = None
        cls.excelStoryDialog = None
        cls.excelGameGuide = None
        cls.excelCardPool = None
        cls.excelWorld = None
        cls.excelCastleSupplyDepot = None
        cls.excelResourcePathDefine = None
        # 删