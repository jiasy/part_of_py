from BB.app.services.BBTs.BBTs_Config.ConfgClass.GameGuide.GameGuideGroup_Sheet import GameGuideGroup_Sheet
from BB.app.services.BBTs.BBTs_Config.Check_GameGuide.GameGuideStep import GameGuideStep
from utils.infoUtils.InfoColor import InfoColor
from utils.infoUtils.InfoLine import InfoLine


class GameGuideGroup(GameGuideGroup_Sheet):
    def __init__(self, guideRoot_):
        super().__init__("GameGuide", "GameGuideGroup")
        self.stepList: list[GameGuideStep] = []  # 旗下步骤
        self.root = guideRoot_

    # 删
