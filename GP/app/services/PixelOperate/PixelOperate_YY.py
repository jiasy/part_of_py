#!/usr/bin/env python3
from GamePlay.app.services.PixelOperate.PixelOperate import PixelOperate
from utils import pyServiceUtils
import os
import sys
from utils import printUtils

# 移除指定帧的色彩内容
if __name__ == '__main__':
    _svr_PixelOperate: PixelOperate = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_PixelOperate.resPath))
    pyServiceUtils.printSvrCode(__file__)

    _nameSpace = "sample"
    _unitFolder = "/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/UnpackPlistPng/sample/"

    # 最后一个为当前处理的unit，这里记录的是运行时获取到的unit的effect颜色在数组中的位置
    _unitEffectColorList = [
        ["sample_110", ],
    ]
    # 移除人物的序号
    _baseRemoveIdx = 0  # -1 为不移除
    _unitName = _unitEffectColorList[-1][0]  # Unit 名称
    _targetUnitFolder = os.path.join(_unitFolder, _unitName)  # 动作png承载
    if not os.path.exists(_targetUnitFolder):
        printUtils.pError(f"ERROR : {_unitName} 不存在")
        sys.exit(1)

    # 指定移除颜色
    _effectColorClickGetList = []
    if _baseRemoveIdx != -1:
        _pngFile = os.path.join(_targetUnitFolder, f'{_unitName}_{_baseRemoveIdx:03d}.png')
        _effectColorClickGetList = _svr_PixelOperate.getUnitImageColor(_pngFile)

    _imageColors = _svr_PixelOperate.getUnitsImageColor(_targetUnitFolder)  # 获取所有颜色
    _sortedColors = _svr_PixelOperate.displayColors(_imageColors, False)  # 显示颜色以及其对应的序号
    printUtils.printList(_sortedColors)

    # 序号转换回颜色
    _unitEffectColorIdxList = _unitEffectColorList[-1][1:]
    for _i in range(len(_unitEffectColorIdxList)):
        _effectColorClickGetList.append(_sortedColors[_unitEffectColorIdxList[_i]])

    # _effectColorClickGetList.remove((255, 255, 255))
    # _effectColorClickGetList.remove((0, 0, 0))

    # 先输出颜色，看一下，配置到最后一项上再执行。
    if len(_effectColorClickGetList) == 0:
        printUtils.pLog(f"{_unitName} 未指定effect颜色")
        sys.exit(1)

    # 拆分特效和角色
    _resUnitFolder = os.path.join(_svr_PixelOperate.resPath, _nameSpace, _unitName)
    # _svr_PixelOperate.process_images_in_folder(_targetUnitFolder, _effectColorClickGetList, mode="keep", resFolder=_resUnitFolder)  # 保留特效色
    _svr_PixelOperate.process_images_in_folder(_targetUnitFolder, _effectColorClickGetList, mode="remove", resFolder=_resUnitFolder)  # 删除特效色
