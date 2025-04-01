# -*- encoding=utf8 -*-
__author__ = "nobody"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
import sys
import random

if not cli_setup():
    auto_setup(__file__, logdir="/disk/AirTest/ROK", devices=[
            "android://127.0.0.1:5037/8e288ec2?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=ADBTOUCH",
    ], project_root="/disk/AirTest/ROK")



def testCheck():
    _picInfo = exists(Template(r"tpl1606417302436.png", record_pos=(0.033, 0.024), resolution=(1920, 1080)))
    if _picInfo:
        touch((1638,126))# 关闭个人信息
    # 关闭国王技能提示
    closeKingSkill()
    # 判断是否在验证码阶段-------------------------- 有就退出
    _picInfo = exists(Template(r"tpl1605853957345.png", record_pos=(0.329, -0.195), resolution=(1920, 1080)))

    if _picInfo:
        print("校验码等待中")
        sys.exit(1)
        return False
    else:
        print("非校验码状态")
        return True

# 关闭国王技能提示提示
def closeKingSkill():
    _picInfo = exists(Template(r"tpl1606045328437.png", record_pos=(0.001, -0.167), resolution=(1920, 1080)))
    if _picInfo:
        touch(_picInfo)

# 判断是否在主城中 -------------------------- 在就出去
def getOutCity():
    _picInfo = exists(Template(r"tpl1605867526720.png", threshold=1.0, rgb=True, record_pos=(-0.452, 0.141), resolution=(1920, 1080)))
    if not _picInfo:
        _picInfo = exists(Template(r"tpl1605870054253.png", record_pos=(-0.449, 0.233), resolution=(1920, 1080)))
        if _picInfo:
            touch(_picInfo)
            print("出主城")
            sleep(4)
    else:
        print("主城外")

# 判断是否在主城中 -------------------------- 不在就进  
def getInCity():
    _picInfo = exists(Template(r"tpl1605863712249.png", threshold=1.0, rgb=True, record_pos=(-0.451, 0.141), resolution=(1920, 1080)))
    if not _picInfo:
        _picInfo = exists(Template(r"tpl1605863793217.png", record_pos=(-0.451, 0.231), resolution=(1920, 1080)))
        if _picInfo:
            touch(_picInfo)
            print("进主城")
            sleep(4)
    else:
        print("主城中")
        
# 招募
def getRecruit():
    _openBtn = r"tpl1605872431537.png"
    def clickConfirm():
        # 确认键
        _picInfo = exists(Template(r"tpl1605872549764.png", record_pos=(-0.193, 0.203), resolution=(1920, 1080)))
        if _picInfo:
            print("确认返回")
            touch(_picInfo)

    # 招募建筑上有招募字样
    _picInfo = exists(Template(r"tpl1605871976275.png", record_pos=(-0.05, -0.056), resolution=(1920, 1080)))
    if _picInfo:
        print("可进行招募")
        touch(_picInfo)
        print("点击招募建筑")
        sleep(1)
        # 弹出三个按钮中，右侧的招募头像按钮
        _picInfo = exists(Template(r"tpl1605872083457.png", record_pos=(0.06, 0.084), resolution=(1920, 1080)))
        if _picInfo:
            print("进入招募界面")
            touch(_picInfo)
            sleep(4)
        # 切换到箱子界面里面后 --------------------------
        # 有装备 --------------------------
        # 有银箱子
        _picInfo = exists(Template(_openBtn, record_pos=(-0.292, 0.191), resolution=(1920, 1080)))
        if _picInfo:
            print("点击银箱子")
            touch(_picInfo)
            print("开箱中")
            sleep(6)
            clickConfirm()

        # 有金钥匙箱子
        _picInfo = exists(Template(_openBtn, record_pos=(0.002, 0.19), resolution=(1920, 1080)))
        if _picInfo:
            print("点击金箱子")
            touch(_picInfo)
            print("开箱中")
            sleep(6)
            clickConfirm()

        # 有装备箱子
        _picInfo = exists(Template(_openBtn, record_pos=(0.295, 0.192), resolution=(1920, 1080)))
        if _picInfo:
            print("点击装备箱子")
            touch(_picInfo)
            print("开箱中")
            sleep(6)
            clickConfirm()
        # 无装备 --------------------------



        # 退出界面
        _picInfo = exists(Template(r"tpl1605872734389.png", record_pos=(-0.469, -0.252), resolution=(1920, 1080)))
        if _picInfo:
            print("退出招募界面")
            touch(_picInfo)
            sleep(4)
    else:
        print("没有可招募对象")

#获取城内资源
def getResources():
    # 收矿，帮助
    _picInfo = exists(Template(r"tpl1605854592926.png", record_pos=(0.107, 0.053), resolution=(1920, 1080)))
    if _picInfo:
        touch(_picInfo)
        print("收石头")

    _picInfo = exists(Template(r"tpl1605854601104.png", record_pos=(0.188, 0.108), resolution=(1920, 1080)))
    if _picInfo:
        touch(_picInfo)
        print("收金币")

    _picInfo = exists(Template(r"tpl1605854607404.png", record_pos=(0.269, 0.167), resolution=(1920, 1080)))
    if _picInfo:
        touch(_picInfo)
        print("收木材")

    _picInfo = exists(Template(r"tpl1605855956907.png", record_pos=(0.132, -0.015), resolution=(1920, 1080)))
    if _picInfo:
        touch(_picInfo)
        print("收玉米")

    _picInfo = exists(Template(r"tpl1605858128134.png", record_pos=(-0.083, 0.094), resolution=(1920, 1080)))
    if _picInfo:
        touch(_picInfo)
        print("点帮助")

#买东西，是否是小号
def buy(isSmall_:bool = False):
    # 一个一个买
    def buyOneByOne(type_:str,line_:int):
        # 第一行的四个按钮位置
        _posList1 = [
            (-0.174, 0.04),
            (-0.03, 0.04),
            (0.113, 0.04),
            (0.257, 0.04)
        ]
        # 滑动后，第三行的四个按钮位置
        _posList2 = [
            (-0.174, 0.213),
            (-0.03, 0.213),
            (0.113, 0.213),
            (0.257, 0.213)
        ]

        _posList = []
        # 不是第一行，就是第三行了
        if line_ == 1:
            _posList = _posList1
        else:
            _posList = _posList2

        for _i in range(len(_posList)):
            _picInfo = exists(Template(type_, threshold=0.9, rgb=False, record_pos=_posList[_i], resolution=(1920, 1080)))
            if _picInfo:
                touch(_picInfo)
                print(str(line_)+":"+str(_i+1))
    # 买一行，买哪一行
    def buyLine(line_:int):
        _corn = r"tpl1605940013786.png" #玉米图标
        _wood = r"tpl1605940021013.png" #木头图标
        buyOneByOne(_corn,line_)
        buyOneByOne(_wood,line_)

    #买第一第三行
    def buyLines(justBuyOne_:bool = False):
        buyLine(1)
        sleep(2)
        if justBuyOne_ == False:# 不是只买第一行
            # 滑动到下面
            swipe(Template(r"tpl1605943415852.png", record_pos=(0.07, 0.213), resolution=(1920, 1080)), vector=[0, -2])
            sleep(4)
            buyLine(3)
            sleep(2)

    _picInfo = exists(Template(r"tpl1605942492044.png", record_pos=(-0.266, 0.078), resolution=(1920, 1080)))
    if _picInfo:
        touch(_picInfo)
        print("点商店")
        
        # 商人不在
        _picInfo = exists(Template(r"tpl1606100512459.png", record_pos=(0.042, -0.057), resolution=(1920, 1080)))
        if _picInfo:
            touch(Template(r"tpl1606100651589.png", record_pos=(0.233, -0.141), resolution=(1920, 1080)))
            print("点商人不在界面的×")
        else:
            _picInfo = exists(Template(r"tpl1605939905978.png", record_pos=(-0.201, 0.189), resolution=(1920, 1080)))
            if _picInfo:
                touch(_picInfo)
                print("进商店")
                sleep(2)
                buyLines(isSmall_)#买买买

                # 刷新按钮为蓝色，免费刷新
                _picInfo = exists(Template(r"tpl1605941007102.png", record_pos=(0.289, -0.154), resolution=(1920, 1080)))
                if _picInfo:
                    touch(_picInfo)
                    print("刷新商店")
                    sleep(2)
                    buyLines(isSmall_)#买买买

                # 退出
                _picInfo = exists(Template(r"tpl1605941015804.png", record_pos=(0.353, -0.218), resolution=(1920, 1080)))
                if _picInfo:
                    touch(_picInfo)
                    print("退出商店")

                    # 商人离开提示框，需要点掉（正在买的时候离开了）
                    _picInfo = exists(Template(r"tpl1605944507861.png", record_pos=(0.002, 0.087), resolution=(1920, 1080)))
                    if _picInfo:
                        touch(_picInfo)
                        print("商人离开提示")

# 医疗
def medical():
    _picInfo = exists(Template(r"tpl1605946873466.png", threshold=0.9, rgb=True, record_pos=(0.024, -0.016), resolution=(1920, 1080)))
    if _picInfo:
        touch(_picInfo)
        sleep(1)
        # 点医疗
        touch(Template(r"tpl1605946888419.png", record_pos=(0.243, 0.162), resolution=(1920, 1080)))
        sleep(1)
        # 点击帮助
        touch(Template(r"tpl1605946903931.png", record_pos=(0.027, -0.004), resolution=(1920, 1080)))

# 是否有空白队列
def haveBlankQueue():
    # 刷默认位置
    getInCity()# 进城
    getOutCity()# 出城
    touch((1189,511),duration=3)# 按住一段时间
    # 迁城 行军 界面中的按钮出现
    _picInfo = exists(Template(r"tpl1606392853173.png", record_pos=(-0.065, 0.048), resolution=(1920, 1080)))
    if _picInfo:
        touch(_picInfo)
        print("点击行军")
        # 还有空队列
        _picInfo = checkBlankQueue()
        # 无论是否能创建队列，都要返回到正常状态。
        touch((100,100))
        if _picInfo:
            print("可创建队列")
            return True
        else:
            print("队列已满，点外侧取消")
            return False
    else:
        print("ERROR - 城堡周围长按失败")
        sys.exit(1)

# 是否还有空队列
def checkBlankQueue():
    # 创建队列按钮存在，还有空队列可用
    _picInfo = exists(Template(r"tpl1605949885936.png", record_pos=(0.287, -0.172), resolution=(1920, 1080)))
    if _picInfo:
        return _picInfo
    else:
        return None

#采集
def collection():
    _searchIcon = r"tpl1605947492608.png"
    _maxLvInMap = 6 # 当前地图最大矿脉等级
    _cancelSearchBtn = r"tpl1605949257398.png"

    def resetLowestLV():
        print("重置到最低等级")
        # 点击搜索
        touch(Template(_searchIcon, record_pos=(-0.452, 0.14), resolution=(1920, 1080)))
        touch((669,954))# 点击玉米
        # 到 1 级别，需要按 _maxLvInMap 下  减号
        # for _i in range(_maxLvInMap):
        touch(Template(r"tpl1606642060989.png", record_pos=(-0.258, 0.034), resolution=(1920, 1080)),times = _maxLvInMap)
        # 退出搜索状态
        touch(Template(_cancelSearchBtn, record_pos=(-0.468, -0.252), resolution=(1920, 1080)))

    def resetLV(to_:int):
        # 点击搜索
        touch(Template(_searchIcon, record_pos=(-0.452, 0.14), resolution=(1920, 1080)))
        sleep(1)
        touch((669,954))# 点击玉米
        sleep(1)
        # 点击 _maxLvInMap 加号
        # for _i in range(_maxLvInMap):
        touch(Template(r"tpl1606642161508.png", record_pos=(-0.043, 0.032), resolution=(1920, 1080)),times=_maxLvInMap)
        # 到 to_ 级别，需要按 _maxLvInMap - to_ 下  减号
        # for _i in range((_maxLvInMap-to_)):
        touch(Template(r"tpl1606642060989.png", record_pos=(-0.258, 0.034), resolution=(1920, 1080)),times = (_maxLvInMap-to_))
        # 退出搜索状态
        touch(Template(_cancelSearchBtn, record_pos=(-0.468, -0.252), resolution=(1920, 1080)))
        
    def collectWhich(type_:int = 0):
        _picInfo = exists(Template(_searchIcon, record_pos=(-0.452, 0.14), resolution=(1920, 1080)))
        if _picInfo:
            print("点击搜索")
            touch(_picInfo)
            if not type_ == 0:
                _whichInt = type_
            else:
                # _randomTypeList = [3,3,4,4,4,4,4] # 最强执政官 采集
                # _randomTypeList = [1,2,3,4] # 平均
                _randomTypeList = [1,1,1,2,2,2,3,3,4] # 食物木材
                _whichIdx = random.randint(0,len(_randomTypeList)-1)
                _whichInt = _randomTypeList[_whichIdx]

            # _whichInt = 1 # 强制种类

            if _whichInt == 1:
                print("    玉米")
                touch((669,954))# 点击玉米
                touch((672,728))# 点击玉米的搜索
            elif _whichInt == 2:
                print("    木头")
                touch((959,956))# 点击木头
                touch((960,728))# 点击木头的搜索
            elif _whichInt == 3:
                print("    石头")
                touch((1250,952))# 点击石头
                touch((1248,728))# 点击石头的搜索
            elif _whichInt == 4:
                print("    金子")
                touch((1535,955))# 点击金子
                touch((1533,728))# 点击金子的搜索
            else:
                sys.exit(1)

            sleep(4)

            # 判断是否还在搜索模式，以确定，是否再循环一次
            _picInfo = exists(Template(_cancelSearchBtn, record_pos=(-0.468, -0.252), resolution=(1920, 1080)))
            if _picInfo:
                print("    没有可用矿产，退出搜索模式")
                touch(_picInfo)
                sleep(10)
                return False
            else:
                print("    自动退出搜索模式，证明有矿")
                return True
        else:
            print("没有搜索按钮")
            return False

    def doCollection():
        touch((1920/2,1080/2),1)
        print("点击屏幕中心矿场")
        sleep(1)
        _picInfo = exists(Template(r"tpl1605949870853.png", record_pos=(0.245, 0.095), resolution=(1920, 1080)))
        if _picInfo:
            print("    点击采集")
            touch(_picInfo)
        else:
            print("    无法采集【自己已经开始挖了，或者别人在搜索的时候进去了】。再次点击矿取消")
            touch((1920/2,1080/2),1)
            return False
        sleep(1)
        # 还有空队列
        _picInfo = checkBlankQueue()
        if _picInfo:
            print("可创建队列")
            touch(_picInfo)
            print("    创建队列")
            sleep(1)
            touch(Template(r"tpl1605949905582.png", record_pos=(0.226, 0.201), resolution=(1920, 1080)))
            print("    点击行军")
            return True
        else:
            touch((100,100))
            print("队列已满，点外侧取消")
            return False
    
    getOutCity()# 出城
    
    resetLV(2)# 重置挖矿等级 -- 失落之地时 2 -> 6级

    # resetLowestLV() # 脚本采集底的也没事儿

    _whichMine = 0 # 指定矿种，0为随机
    while collectWhich(_whichMine) == False: # 没有找到可用矿就再找一次
        continue
    while doCollection():# 能派队列就继续
        while collectWhich(_whichMine) == False: # 没有找到可用矿就再找一次
            continue
    print("采集队列派遣完毕")

# 打开联盟界面
def clickAlliance():
    # 联盟的按钮
    _allianceBtn = r"tpl1606011076264.png"
    _picInfo = exists(Template(_allianceBtn, threshold=0.9, rgb=False, record_pos=(0.306, 0.244), resolution=(1920, 1080)))
    if not _picInfo: # 展开联盟按钮
        print("    没有联盟按钮")
        touch(Template(r"tpl1606011089843.png", record_pos=(0.463, 0.241), resolution=(1920, 1080)))
        print("    切换出联盟按钮")
        sleep(1)
    else:
        print("    存在联盟按钮")
    # 点击联盟按钮
    touch(Template(_allianceBtn, record_pos=(0.463, 0.241), resolution=(1920, 1080)))
    print("    点击联盟按钮")
    sleep(2)


# 退出联盟界面，退出联盟内界面的通用方法
def quitAllianceUI():
    touch((1676,65))# 退出界面
    sleep(1)

# 处理，联盟界面内的内容
def dealWithAlliance():
    def getGift():
        # 进入领取奖励界面
        touch(Template(r"tpl1606013611055.png", record_pos=(0.192, 0.156), resolution=(1920, 1080)))
        sleep(2)
        # 领取普通奖励 -----------------------------------------
        touch((1007,304))# 普通按钮
        sleep(1)
        touch((1672,315))# 一键领取
        sleep(1)
        touch((966,793))# 一键领取后的确定
        sleep(1)
        # 领取稀有奖励 -----------------------------------------
        touch((1391,307))# 稀有按钮
        sleep(1)
        touch((1459,422))# 第一个领取
        sleep(1)
        while True:# 第二个领取，一直领取到没有为止
            _picInfo = exists(Template(r"tpl1606014040607.png", record_pos=(0.26, 0.013), resolution=(1920, 1080)))
            if _picInfo:
                touch(_picInfo)
                sleep(1)
            else:
                break
        quitAllianceUI()# 退出联盟子界面
    
    def getLandResource():
        # 进入领地收益界面
        touch(Template(r"tpl1606015210614.png", record_pos=(0.193, 0.038), resolution=(1920, 1080)))
        sleep(1)
        touch((1526,208))# 点击领取
        sleep(1)
        quitAllianceUI()# 退出联盟子界面

    print("处理联盟内容")
    clickAlliance()# 确保进入联盟界面
    getGift()# 领取联盟奖励
    getLandResource()# 获取领地收益
    quitAllianceUI()# 退出联盟界面

# 日常任务完成
def getTaskRewards():
    print("处理日常任务")
    # 点击任务
    touch(Template(r"tpl1606022416813.png", record_pos=(-0.463, -0.152), resolution=(1920, 1080)))
    sleep(1)
    touch((160,473))# 点击日常
    sleep(1)
    while True:# 直领取到没有为止
        _picInfo = exists(Template(r"tpl1606022440416.png", record_pos=(0.286, -0.017), resolution=(1920, 1080)))
        if _picInfo:
            touch(_picInfo)
            sleep(1)
        else:
            break
    touch((1637,125))# 点击退出


# 切换 预制 队伍。1-蓝:打野，2-红:山寨，3-黄:远征
def switchPreQueue(which_:int):
    _blue = r"tpl1606045794993.png"
    _red = r"tpl1606045805366.png"
    _yellow = r"tpl1606045782708.png"
    if which_ == 1:# 蓝
        _current = _blue
    elif which_ == 2:# 红
        _current = _red
    elif which_ == 3:# 黄
        _current = _yellow

    _count = 0
    _picInfo = exists(Template(_current, threshold=0.85, rgb=True,record_pos=(0.362, -0.029), resolution=(1920, 1080)))
    while not _picInfo:
        _count = _count + 1
        if _count > 2:
            print("    预制队列，寻找颜色错误 - X")
            return False
        touch((1652,397))# 切换颜色
        sleep(1)
        _picInfo = exists(Template(_current, threshold=0.85, rgb=True,record_pos=(0.362, -0.029), resolution=(1920, 1080)))
    return True

# 按下哪一个预制队列
def clickPreQueue(which_:int):
    if which_ == 1:
        touch((1655,481))# 右侧队列 1 选项
    elif which_ == 2:
        touch((1655,571))# 右侧队列 2 选项
    elif which_ == 3:
        touch((1655,653))# 右侧队列 3 选项
    elif which_ == 4:
        touch((1656,741))# 右侧队列 4 选项
    elif which_ == 5:
        touch((1655,833))# 右侧队列 5 选项
    else:
        print("ERROR - 预制队列，序号错误")
        sys.exit(1)

def dealWithWar():
    # 加入集结
    def joinWar():
        touch(Template(r"tpl1606043444405.png", record_pos=(-0.014, 0.035), resolution=(1920, 1080)))
        print("    点击战争")
        sleep(1)
        _picInfo = exists(Template(r"tpl1606043459560.png", threshold=0.95, rgb=True, record_pos=(0.307, -0.145), resolution=(1920, 1080)))
        if _picInfo:
            print("    第一个，是山寨")
            _picInfo = exists(Template(r"tpl1606044976213.png", threshold=0.85, rgb=True, record_pos=(-0.199, -0.114), resolution=(1920, 1080)))
            if _picInfo:
                print("    还可以加入，绿色进度条")
                touch(_picInfo)
                print("    点击加入")
                sleep(2)
                _picInfo = checkBlankQueue()
                if _picInfo:# 还有空队列
                    print("    可创建队列")
                    touch(_picInfo)
                    print("    创建队列")
                    sleep(1)
                    print("    从预制队列中筛选。1-蓝:打野，2-红:山寨，3-黄:远征")
                    if switchPreQueue(2):
                        sleep(1)
                        print("    选着预制队列的第一个预制")
                        clickPreQueue(1)
                        sleep(1)
                        # 红色队列的第一个位置选中后，图标是粉色的。
                        _picInfo = exists(Template(r"tpl1606047055370.png", threshold=0.85, rgb=True, record_pos=(0.362, -0.028), resolution=(1920, 1080)))
                        if _picInfo:
                            print("    成功选着预制队列")
                            touch(Template(r"tpl1605949905582.png", record_pos=(0.226, 0.201), resolution=(1920, 1080)))
                            print("    点击行军")
                            sleep(2)
                            # 路途遥远提示的那个红蓝按钮截图
                            _picInfo = exists(Template(r"tpl1606048600899.png", threshold=0.9, rgb=True, record_pos=(0.109, 0.113), resolution=(1920, 1080)))
                            if not _picInfo:
                                # 体力补充界面和队列界面叠加的那个右上角截图
                                _picInfo = exists(Template(r"tpl1606131989531.png", threshold=0.9, rgb=True, record_pos=(0.351, -0.217), resolution=(1920, 1080)))
                                if not _picInfo:
                                    print("    成功出发")
                                else:
                                    print("    体力不足")
                                    touch((1638,126))# 关闭体力界面
                                    print("    关闭体力界面")
                                    sleep(2)
                                    touch((1676,75))# 关闭队列选择
                                    print("    关闭队列选择")
                            else:
                                print("    路途遥远")
                                touch(_picInfo)
                                print("    选择否")
                        else:
                            print("    预设队列已在使用")
                            touch((1676,75))# 关闭队列选择
                            print("    关闭队列选择")
                    else:
                        print("    队列切换失败")
                        touch((1676,75))# 关闭队列选择
                        print("    关闭队列选择")
                else:
                    print("    不可创建队列")
                    touch((100,100))
                    print("    点外侧取消")
            else:
                print("    不可以加入，非绿色状态")
                quitAllianceUI()# 退出联盟子界面
                print("    退出战争界面")
                sleep(1)
                quitAllianceUI()# 退出联盟界面
                print("    退出联盟界面")
        else:
            print("    第一个，不是山寨")
            quitAllianceUI()# 退出联盟子界面
            print("    退出战争界面")
            sleep(1)
            quitAllianceUI()# 退出联盟界面
            print("    退出联盟界面")
        sleep(2)
        _picInfo = exists(Template(r"tpl1606462545536.png", record_pos=(0.352, -0.217), resolution=(1920, 1080)))
        if _picInfo:
            print("    金币界面跳出 - 将它关闭")
            touch(_picInfo)

    print("处理战争")
    clickAlliance()# 确保进入联盟界面
    joinWar()# 加入战争

def autoInTheDayTime():
    while testCheck():
        # -----------------------------------
        getInCity()# 城市内
        getRecruit()# 招募
        getResources()# 收集
        # buy(False)# 商人 - 非小号
        medical()# 治疗
        # -----------------------------------
        # 有空队列
        if haveBlankQueue():
            dealWithWar()# 集结山寨
            collection()
        # -----------------------------------
        getTaskRewards()# 领日常任务奖励
        dealWithAlliance()# 联盟
        print("等待 250 秒")
        sleep(250)

def autoInTheDayTimeJustQueue():
    while testCheck():
        # 有空队列
        if haveBlankQueue():
            # -----------------------------------
            dealWithWar()# 集结山寨
            collection()
        print("等待 300 秒")
        sleep(300)

def autoInNightTime():
    while testCheck():
        # 有空队列
        if haveBlankQueue():
            # -----------------------------------
            # dealWithWar()# 集结山寨
            collection()
        print("等待 300 秒")
        sleep(300)

# # 白天执行内容
# autoInTheDayTime()

# 白天内容，仅管理队列，采集和战争
autoInTheDayTimeJustQueue()

# # 夜间执行内容，只是采集
# autoInNightTime()

# _picInfo = exists(Template(r"tpl1605948589238.png", record_pos=(-0.15, 0.099), resolution=(1920, 1080)))
# print("touch("+str(_picInfo[0])+","+str(_picInfo[1])+")")





















g