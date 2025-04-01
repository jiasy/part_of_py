# !/usr/bin/env python3
import sys

from GamePlay.app.services.UnpackPlistPng.UnpackPlistPng import UnpackPlistPng
from utils import pyServiceUtils
from utils import folderUtils
from utils import printUtils
from utils import fileCopyUtils
from utils import imageUtils
import shutil
import os

actNameList = ["attack", "breathing", "breathe", "breath", "death", "hit", "idle", "run", "projectile",
               "castendsample", "castend", "castLoop", "castloop", "casting", "castStart", "caststart", "cast",
               "damage", "hurt", "die", "crawl", "open", "move", "explode", "movement"]


# -----------------------------------------------------------------------------------------------------------------------
# Sample 特有的 png 文件结构，将 unit 文件夹下的 png 按照动作分文件夹
def unitPngToSubFolder(pngFolder_):
    _unitNameList = folderUtils.getFolderNameListJustOneDepth(pngFolder_)
    for _idx in range(len(_unitNameList)):
        _unitName = _unitNameList[_idx]  # unit 的名称
        _unitPngFolder = os.path.join(pngFolder_, _unitName)  # unit 的图片文件夹
        _unitPngList = folderUtils.getFileNameListJustOneDepth(_unitPngFolder, [".png"])  # 所有 png 名称
        if len(_unitPngList) > 0:
            printUtils.pError(f"{_unitName}")
        for _idxLoop in range(len(actNameList)):
            _actName = actNameList[_idxLoop]  # 动作的 png 列表
            _actPngNameList = []  # 当前动作的逐帧图
            for _idxPngLoop in range(len(_unitPngList)):
                _pngName = _unitPngList[_idxPngLoop]
                if _pngName.startswith(f'{_unitName}_{_actName}_'):
                    _actPngNameList.append(_pngName)
            if len(_actPngNameList) > 0:
                _unitActPngFolder = os.path.join(_unitPngFolder, _actName)  # unit 的动作
                folderUtils.makeSureDirIsExists(_unitActPngFolder)
                for _idxPngLoop in range(len(_actPngNameList)):
                    _src = os.path.join(_unitPngFolder, _actPngNameList[_idxPngLoop])
                    _tar = os.path.join(_unitActPngFolder, _actPngNameList[_idxPngLoop])
                    shutil.move(_src, _tar)


# -----------------------------------------------------------------------------------------------------------------------
# unit 的主文件夹 ，将其中的所有动作转成对应的 gif
def unitPngToActGif(unitPngFolder_):
    _unitNameList = sorted(folderUtils.getFolderNameListJustOneDepth(unitPngFolder_))
    for _idx in range(len(_unitNameList)):
        _unitName = _unitNameList[_idx]  # unit 的名称
        _unitPngFolder = os.path.join(unitPngFolder_, _unitName)  # unit 主文件夹
        pngToGif(_unitPngFolder)


# 每一个 png子文件夹 转一个 gif
def pngToGif(pngFolder_):
    _foldNameList = folderUtils.getFolderNameListJustOneDepth(pngFolder_)  # 每一个动作的名称
    for _idxLoop in range(len(_foldNameList)):
        _folderName = _foldNameList[_idxLoop]
        _pngSubFolder = os.path.join(pngFolder_, _folderName)  # 动作子文件夹
        print('_pngSubFolder = ' + str(_pngSubFolder))
        _gifPath = os.path.join(pngFolder_, f'{_folderName}.gif')
        if not os.path.exists(_gifPath):
            imageUtils.pngFolderToGif(_pngSubFolder, _gifPath, 12)


# -----------------------------------------------------------------------------------------------------------------------
# Sample 的Gif按照动作分文件夹
def placeGifToActionFolder(unitGifFolder_, actionGifFolder_):
    if not os.path.exists(unitGifFolder_):
        printUtils.pError(f"unitGifFolder_ 不存在")
        sys.exit(1)
    if not os.path.exists(actionGifFolder_):
        printUtils.pError(f"actionGifFolder_ 不存在")
        sys.exit(1)
    _unitNameList = folderUtils.getFolderNameListJustOneDepth(unitGifFolder_)  # 每一个角色的名称
    for _i in range(len(_unitNameList)):
        _unitName = _unitNameList[_i]
        _unitFolder = os.path.join(unitGifFolder_, _unitName)
        for _idx in range(len(actNameList)):
            _actionName = actNameList[_idx]
            _actionGifSrc = os.path.join(_unitFolder, f'{_actionName}.gif')
            if os.path.exists(_actionGifSrc):
                _actionGifTarget = os.path.join(actionGifFolder_, _actionName)
                folderUtils.makeSureDirIsExists(_actionGifTarget)
                fileCopyUtils.copyFile(_actionGifSrc, os.path.join(_actionGifTarget, f'{_unitName}.gif'))


if __name__ == '__main__':
    _svr_UnpackPlistPng: UnpackPlistPng = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_UnpackPlistPng.resPath))
    pyServiceUtils.printSvrCode(__file__)

    _nameSpace = "SAMPLE"
    # # 拆分 plist 图片
    # _srcPlistFolder = "/Users/GD/Documents/develop/ART/SAMPLE-main/app/resources/"
    # _svr_UnpackPlistPng.plistFolderToPngFolder(_srcPlistFolder, _nameSpace)

    # # 打印 unit 内容
    # _nameList = folderUtils.getFolderNameListJustOneDepth("/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/UnpackPlistPng/SAMPLE/units/")
    # printUtils.printList(sorted(_nameList))

    # # 把动作分类放入子文件夹
    # unitPngToSubFolder(os.path.join(_svr_UnpackPlistPng.resPath, _nameSpace, "units"))

    # # units 的动作图片转换成 gif
    # unitPngToActGif(os.path.join(_svr_UnpackPlistPng.resPath, _nameSpace, "units"))
    # # 特效 等 转 gif
    # pngToGif(os.path.join(_svr_UnpackPlistPng.resPath, _nameSpace, "fx"))
    # pngToGif(os.path.join(_svr_UnpackPlistPng.resPath, _nameSpace, "icons"))
    # pngToGif(os.path.join(_svr_UnpackPlistPng.resPath, _nameSpace, "runes"))
    # pngToGif(os.path.join(_svr_UnpackPlistPng.resPath, _nameSpace, "tiles"))

    # # 拷贝图片
    # fileCopyUtils.copyFilesInFolderTo(
    #     [".gif"],
    #     "/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/UnpackPlistPng/SAMPLE/units/",
    #     "/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/UnpackPlistPng/SAMPLE/units_gif/",
    #     "include", True
    # )

    placeGifToActionFolder("/Users/GD/Documents/develop/ART/当前资源/SAMPLE_units_gif", "/Users/GD/Documents/develop/ART/当前资源/SAMPLE_action_gif")
