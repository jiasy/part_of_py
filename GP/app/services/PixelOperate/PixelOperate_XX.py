#!/usr/bin/env python3
from GamePlay.app.services.PixelOperate.PixelOperate import PixelOperate
from utils import pyServiceUtils
import os
from utils import printUtils
import sys

if __name__ == '__main__':
    _svr_PixelOperate: PixelOperate = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_PixelOperate.resPath))
    pyServiceUtils.printSvrCode(__file__)

    _nameSpace = "SAMPLE"
    _unitFolder = "/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/UnpackPlistPng/SAMPLE/icons/icon_icon/"
    _unitFolder = "/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/UnpackPlistPng/sample/"

    # 最后一个为当前处理的unit，这里记录的是运行时获取到的unit的effect颜色在数组中的位置
    _unitEffectColorList = [
        ["sample_76", 10,11,24,17,0,5,6,9,],
    ]
    _effectColorClickGetList = [
        # # (252, 255, 255),
        # (200, 247, 248), (168, 207, 214), (150, 178, 195), (136, 154, 174), (29, 41, 61),
        # # (98, 80, 126), (129, 112, 154), (160, 150, 209),  # icon_n1
        # (10, 11, 15), (20, 22, 31), (61, 66, 101), (41, 44, 66), (30, 33, 49),  # icon_f6
        # # (30, 21, 22), (54, 37, 41), (76, 66, 58), (120, 107, 98),  # icon_f3
        # (0, 0, 0), (29, 57, 148),
    ]
    _unitName = _unitEffectColorList[-1][0]  # Unit 名称
    _targetUnitFolder = os.path.join(_unitFolder, _unitName)  # 动作png承载
    if not os.path.exists(_targetUnitFolder):
        printUtils.pError(f"ERROR : {_unitName} 不存在")
        sys.exit(1)

    _imageColors = _svr_PixelOperate.getUnitsImageColor(_targetUnitFolder)  # 获取所有颜色
    _sortedColors = _svr_PixelOperate.displayColors(_imageColors, False)  # 显示颜色以及其对应的序号
    printUtils.printList(_sortedColors)

    # 序号转换回颜色
    _unitEffectColorIdxList = _unitEffectColorList[-1][1:]
    for _i in range(len(_unitEffectColorIdxList)):
        _effectColorClickGetList.append(_sortedColors[_unitEffectColorIdxList[_i]])

    # 先输出颜色，看一下，配置到最后一项上再执行。
    if len(_effectColorClickGetList) == 0:
        printUtils.pLog(f"{_unitName} 未指定effect颜色")
        sys.exit(1)

    # # 临时展示，看看选的对不对
    # tempDisPlay(
    #     "/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/UnpackPlistPng/SAMPLE/units/boss_borealjuggernaut/attack/boss_borealjuggernaut_attack_013.png",
    #     _effectColors
    # )
    # sys.exit(1)

    # 拆分特效和角色
    _resUnitFolder = os.path.join(_svr_PixelOperate.resPath, _nameSpace, _unitName)
    _svr_PixelOperate.process_images_in_folder(_targetUnitFolder, _effectColorClickGetList, mode="remove", resFolder=_resUnitFolder)  # 删除特效色
    _svr_PixelOperate.process_images_in_folder(_targetUnitFolder, _effectColorClickGetList, mode="keep", resFolder=_resUnitFolder)  # 保留特效色
