from BB.app.services.BBTs.BBTs_Config.ConfgClass.GameGuide.GameGuideStep_Sheet import GameGuideStep_Sheet
from FGUI.fguiUtils import fguiDisPathUtils
from utils.infoUtils.InfoColor import InfoColor
from utils.infoUtils.InfoLine import InfoLine
from utils import folderUtils
from utils import fileUtils


class GameGuideStep(GameGuideStep_Sheet):
    def __init__(self, guideRoot_):
        super().__init__("GameGuide", "GuideGuideStep")
        self.root = guideRoot_

    def toDict(self):
        print(f"        Step toDict : {self.Id}")
        _dict = super().toDict()
        return _dict

    def checkBuildingOrBlock(self):
        # 删

    def checkWidget(self, widgetPath_: str, checkClickBool_: bool, checkIsGroup_: bool):
        if widgetPath_.strip() == "":
            print(f"ERROR : step [{self.RowIdFromPy}] {self.Id} - {self.Type} - 普通点击 - Widget 为多个空格")
        _pkg_cmp_names = self.ResPath.split("/")
        _findWidget = widgetPath_
        _widgetFirstPart = widgetPath_.split(".")[0]
        if "@" in _widgetFirstPart:
            _first_widget_pkg_cmp_names = _widgetFirstPart.split("@")  # 命名规则，反向得到其pkg和cmp
            if _pkg_cmp_names[0] == _first_widget_pkg_cmp_names[1] and _pkg_cmp_names[1] == _first_widget_pkg_cmp_names[0]:
                print(f"ERROR : step [{self.RowIdFromPy}] {self.Id} - {self.Type} - 普通点击 - {self.ResPath} 和 {_widgetFirstPart} 指向同一个组件。子UI不可能是自己，这样会无限嵌套")
        _displayKey, _displayDict = fguiDisPathUtils.getDisplayKeyOnPath(self.root.fguiProject, _pkg_cmp_names[0], _pkg_cmp_names[1], _findWidget, checkClickBool_)
        if "(" not in widgetPath_:
            if _displayKey is None:  # 不是方法，是UI路径的时候，校验这路径
                print(f"ERROR : step [{self.RowIdFromPy}] {self.Id} - {self.Type} - 普通点击 - {self.ResPath} - {widgetPath_} 配置错误")
            else:
                if checkIsGroup_:  # 需要检查组
                    if _displayKey != "group":  # 不是组
                        print(f"ERROR : step [{self.RowIdFromPy}] {self.Id} - {self.Type} - 普通点击 - {self.ResPath} - {widgetPath_} 不是一个 组")
                    else:  # 是组
                        if "@advanced" not in _displayDict or _displayDict["@advanced"] is not True:  # 不是高级组
                            print(f"ERROR : step [{self.RowIdFromPy}] {self.Id} - {self.Type} - 普通点击 - {self.ResPath} - {widgetPath_} 不是一个 高级组")
        else:  # 是一个方法的时候
            _funcName = widgetPath_.split("(")[0]
            for _key in self.root.uiPathDict:
                _value = self.root.uiPathDict[_key]
                if _value == self.ResPath:
                    _tsFilePathList = folderUtils.getFilterFilesInPathReg(self.root.tsFolderPath, [f'\\{_key}\.ts$'])
                    if len(_tsFilePathList) == 0:
                        print(f"ERROR : step [{self.RowIdFromPy}] {self.Id} - {self.Type} - 普通点击 - {self.ResPath} - 未找到其对应的 Layer")
                    else:
                        _findBool = fileUtils.fileHasString(_tsFilePathList[0], _funcName)
                        if not _findBool:
                            print(f"ERROR : step [{self.RowIdFromPy}] {self.Id} - {self.Type} - 普通点击 - {self.ResPath} - {_tsFilePathList[0]} 没有指定方法")

    def check(self):
        # 删

    def getDesc_Id(self, infoLine_: InfoLine):
        infoLine_.addBlank(InfoColor.Red)
        infoLine_.addBlank(InfoColor.Magenta)
        infoLine_.addInfo(f"  {self.Id} --- ", InfoColor.Black, InfoColor.Blue)

    def getDesc_Building_or_Block(self):
        if self.BlockId != 0:
            return self.root.getCastleBlockDesc(self.BlockId)
        else:
            return self.root.getCastleBuildingDesc(self.BuildingId)

    # 是否 和 建筑 或 障碍物 有关
    def isRelationToBuildOrBlock(self):
        if self.Type == 4 or self.Type == 5 or self.Type == 7 or self.Type == 14 or self.Type == 15:
            return True
        return False

    # 获取描述信息
    def getDesc_Info(self, infoLine_: InfoLine):
        # 删

    # 讲解自身功能
    def desc(self):
        # print(f"        Step desc : {self.Id}")
        _infoLine = self.root.info.newLine()
        self.getDesc_Id(_infoLine)
        self.getDesc_Info(_infoLine)
