from BB.app.services.BBTs.BBTs_Config.ConfgClass.CastleBlock.CastleBlock_Sheet import CastleBlock_Sheet
from BB.app.services.BBTs.BBTs_Config.ConfgClass.GameGuide.GameGuide_Sheet import GameGuide_Sheet
from BB.app.services.BBTs.BBTs_Config.ConfgClass.GameMainInterfaceIcon.GameMainInterfaceIcon_Sheet import GameMainInterfaceIcon_Sheet
from BB.app.services.BBTs.BBTs_Config.Check_GameGuide.GameGuideGroup import GameGuideGroup
from BB.app.services.BBTs.BBTs_Config.ConfgClass.ResourcePathDefine.ResourcePathDefine_Sheet import ResourcePathDefine_Sheet
from utils.infoUtils.InfoColor import InfoColor
from utils.infoUtils.InfoLine import InfoLine


class GameGuide(GameGuide_Sheet):
    def __init__(self, guideRoot_):
        super().__init__("GameGuide", "GameGuide")
        self.groupList: list[GameGuideGroup] = []  # 旗下组
        self.root = guideRoot_

    # 返回这个 group 之后的 group 列表
    def getGroupListAfterGroup(self, group_):
        _afterGroupList = []
        _startRecord = False
        for _i in range(len(self.groupList)):
            _group = self.groupList[_i]
            if _startRecord:
                _afterGroupList.append(_group)
            if _group == group_:
                _startRecord = True  # 开始录制
        return _afterGroupList

    def isAnyStepRelationToBuildOrBlock(self):
        _foundBool = False  # 查找自己其下的所有 Group 和 Step
        for _i in range(len(self.groupList)):
            _group = self.groupList[_i]
            for _iLoop in range(len(_group.stepList)):
                _step = _group.stepList[_iLoop]
                if _step.isRelationToBuildOrBlock():  # 如果是和 建筑物 或 障碍物 相关
                    _foundBool = True
                    break
            if _foundBool:
                break
        return _foundBool

    def toDict(self):
        print(f"Guide toDict : {self.Id}")
        _dict = super().toDict()
        _dict["groupList"] = [group.toDict() for group in self.groupList]
        return _dict

    def check(self):
        #删

    def getDesc_Id(self, infoLine_: InfoLine):
        infoLine_.addInfo(f" {str(self.Id).rjust(3)} - ", InfoColor.Black, InfoColor.Red)

    def getDesc_Info(self, infoLine_: InfoLine):
        #删

    def desc(self):
        _infoLine = self.root.info.newLine(True)  # 新组
        self.getDesc_Id(_infoLine)
        self.getDesc_Info(_infoLine)
        for group in self.groupList:
            group.desc()
