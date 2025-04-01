#!/usr/bin/env python3
import sys

import numpy as np

from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
import os
from PIL import Image
import matplotlib.pyplot as plt
from utils import folderUtils
from utils import fileUtils
from utils import printUtils
from utils import fileCopyUtils

import sys
import numpy as np


def modify_image_transparency(image_path, target_colors, tolerance=1, mode='keep', remove_colors_=None):
    # 打开图像
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        # 颜色必除
        if remove_colors_ is not None and not any(all(abs(item[i] - color[i]) <= tolerance for i in range(3)) for color in remove_colors_):
            new_data.append((255, 255, 255, 0))  # 使像素透明
        else:
            # 检查当前像素颜色是否在目标保留颜色中
            if not any(all(abs(item[i] - color[i]) <= tolerance for i in range(3)) for color in target_colors):
                if mode == 'remove':
                    new_data.append(item)  # 保持原像素不变
                else:
                    new_data.append((255, 255, 255, 0))  # 使像素透明
            else:
                if mode == 'remove':
                    new_data.append((255, 255, 255, 0))  # 使像素透明
                else:
                    new_data.append(item)  # 保持原像素不变

    img.putdata(new_data)
    return img


def tempDisPlay(imagePath_, targetColors_):
    # 处理图像
    modified_img = modify_image_transparency(imagePath_, targetColors_, mode="remove")
    # 将修改后的图像转换为 NumPy 数组以便于展示
    img_array = modified_img.convert("RGB")  # 转为 RGB 模式
    img_array = np.array(img_array)
    # 使用 matplotlib 显示图像
    plt.imshow(img_array)
    plt.axis('off')  # 不显示坐标轴
    plt.show()


def movePng(prefix_: str, type_: str):
    _srcFolder = "/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/PixelOperate/SAMPLE/"
    _tarFolder = "/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/UnpackPlistPng/SAMPLE/unitsJust"
    if type_ == "keep" or type_ == "remove":  # 特效 和 角色
        _unitLoopNameList = folderUtils.getFolderNameListJustOneDepth(_srcFolder)
        for _idx in range(len(_unitLoopNameList)):
            _unitLoopName = _unitLoopNameList[_idx]  # 每一个角色
            if _unitLoopName.startswith(prefix_):  # 给定字母开头
                _copySrcUnitFolder = os.path.join(_srcFolder, _unitLoopName, type_)  # 要拷贝的是 特效 还是 角色 本身
                _copyTarUnitFolder = os.path.join(_tarFolder, _unitLoopName)
                if not os.path.exists(_copySrcUnitFolder):
                    printUtils.pError(f"ERROR : {_copySrcUnitFolder} not exist")
                    sys.exit(1)
                fileCopyUtils.copyFilesInFolderTo([".png"], _copySrcUnitFolder, _copyTarUnitFolder)  # 图片直接同结构拷贝过去
            else:
                printUtils.pLog(f"{_unitLoopName} 不满足 {prefix_} 开头")
    else:
        printUtils.pError(f"ERROR : 类型只能是keep或者remove")
        sys.exit(1)


# gif 拆解成 pngs
def gifToPngs(gifPath_, targetFolder_):
    _justName = fileUtils.justName(gifPath_)  # gif 名作为 folder 名称
    with Image.open(gifPath_) as img:
        for frame in range(img.n_frames):
            img.seek(frame)  # 移动到当前帧
            folderUtils.makeSureDirIsExists(os.path.join(targetFolder_, _justName))
            img.save(os.path.join(targetFolder_, _justName, f'{_justName}_{frame:03d}.png'), 'PNG')


class PixelOperate(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(PixelOperate, self).create()

    def destroy(self):
        super(PixelOperate, self).destroy()

    # 获取所有png的颜色
    def getUnitsImageColor(self, imageFolderPath_):
        _pngList = folderUtils.getFileListInFolder(imageFolderPath_, [".png"])
        _colors = set()  # 使用集合避免重复颜色
        for _i in range(len(_pngList)):
            _pngPath = _pngList[_i]
            _pixels = self.getUnitImageColor(_pngPath)
            _colors.update(_pixels)  # 将颜色添加到集合中
        return _colors

    def getUnitImageColor(self, imagePath_):
        try:
            with Image.open(imagePath_) as img:  # 打开图片并获取颜色
                img = img.convert('RGB')  # 转换为RGB模式
                _colors = set()  # 使用集合避免重复颜色
                _colors.update(img.getdata())
                return list(_colors)
        except Exception as e:
            print(f"无法处理文件 {imagePath_}: {e}")
            sys.exit(1)

    # 显示颜色，并标明其序号
    def displayColors(self, colors_, display_=False):
        # 删

    # 将图片的 effect 和 角色分离
    def process_images_in_folder(self, imageFolderPath_, target_colors, tolerance=5, mode='keep', resFolder=None, remove_colors_=None):
        # 删

    def gifFolderToPngFolder(self, gifFolder_, targetFolder_):
        folderUtils.makeSureDirIsExists(targetFolder_)
        _gifFileList = folderUtils.getFileListInFolder(gifFolder_, [".gif"])
        for _i in range(len(_gifFileList)):
            gifToPngs(_gifFileList[_i], targetFolder_)


if __name__ == '__main__':
    _svr_PixelOperate: PixelOperate = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr_PixelOperate.resPath))
    pyServiceUtils.printSvrCode(__file__)

    # _nameSpace = "sample"
    # _gifFolder = "/Users/GD/Documents/develop/ART/dqzy/"
    # _svr_PixelOperate.gifFolderToPngFolder(_gifFolder, os.path.join(_svr_PixelOperate.resPath, _nameSpace))
    # sys.exit(1)

    gifToPngs(
        "/Users/GD/Documents/develop/ART/dqzy/sample_20.gif",
        "/Users/GD/Documents/develop/GitHub/Services/PY_Service/GamePlay/res/services/UnpackPlistPng/sample/sample_20/"
    )
    sys.exit(1)

    # 移动分离好的文件到 flash 导入的文件夹中
    movePng("neutral_", "remove")
    sys.exit(1)
