def CrossBoss():
    _logicType = "NORMAL"
    _pageList = [
        "BossCompetitionMainPage",  # 第一个是主界面
        "BossCompetitionRewardPagePage",
        "BossCompetitionStrategyGuidePage"
    ]
    _protoList = [
        "crossBossCompetition",  # 第一个是主结构
        "user",
        "guild",
        "commonreward",
    ]
    _protoStructList = [
        "BossCompetitionRewardRank",
        "BossCompetitionConfig",
        "BossCompetitionSeason"
    ]
    _funcID = 257001
    _activityID = None
    _common = "业务名称"
    return _logicType, _pageList, _protoList, _protoStructList, _funcID, _activityID, _common


def MonthCardTW():
    _logicType = "NORMAL"
    _pageList = [
        "MonthCardTWPanel",
    ]
    _protoList = [
        "monthcardspec",
        "commonreward",
    ]
    _protoStructList = [
        "MonthlySubscribeTWD",
    ]
    _funcID = 32
    _activityID = None
    _common = "业务名称"
    return _logicType, _pageList, _protoList, _protoStructList, _funcID, _activityID, _common


def LoginReward():
    _logicType = "INTRNAL"
    _pageList = [
        "LoginRewardPanel",
        "LoginRewardItem",
    ]
    _protoList = []
    _protoStructList = []
    _funcID = None
    _activityID = 604001
    _common = "业务名称"
    return _logicType, _pageList, _protoList, _protoStructList, _funcID, _activityID, _common


def DailyRecharge():
    _logicType = "INTRNAL"
    _pageList = [
        "DailyRechargePage",
        "DailyRechargeSection",
    ]
    _protoList = [
        "addrecharge"
    ]
    _protoStructList = [
        "AddRecharge",
    ]
    _funcID = None
    _activityID = 608050
    _common = "业务名称"
    return _logicType, _pageList, _protoList, _protoStructList, _funcID, _activityID, _common


def TreatyGift():
    _logicType = "INTRNAL"
    _pageList = [
        "TreatyGiftPage"
    ]
    _protoList = [
        "activitytreatygift"
    ]
    _protoStructList = [
        "SevenConditionActivity",
        "SevenCondition",
    ]
    _funcID = None
    _activityID = 608080  # - 608081 - 608082 - 608083
    _common = "业务名称"
    return _logicType, _pageList, _protoList, _protoStructList, _funcID, _activityID, _common



def getConfigByName( moduleName_: str):
    if moduleName_ == "CrossBoss":  # 业务名称
        return CrossBoss()
    if moduleName_ == "MonthCardTW":  # 业务名称
        return MonthCardTW()
    if moduleName_ == "LoginReward":  # 业务名称
        return LoginReward()
    if moduleName_ == "DailyRecharge":  # 业务名称
        return DailyRecharge()
    if moduleName_ == "TreatyGift":  # 业务名称
        return TreatyGift()
