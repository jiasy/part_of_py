# !/usr/bin/env python3
import sys
import utils.folderUtils
import utils.fileUtils
import utils.sysUtils
import utils.strUtils
from PIL import Image
from PIL import ImageFile
import math
import utils.numUtils

import os
import cv2
import numpy
import shutil


# 文件转换成没有透明度的jpg
def bmpToJpg(bmpPath_):
    im = Image.open(bmpPath_)
    im.save(
        os.path.join(
            os.path.dirname(bmpPath_),
            utils.fileUtils.justName(bmpPath_) + ".jpg"
        ),
        quality=95
    )


# 文件转换成没有透明度的jpg
def convertToJpg(pngPath_):
    im = Image.open(pngPath_)
    im = im.convert('RGB')
    im.save(
        os.path.join(
            os.path.dirname(pngPath_),
            utils.fileUtils.justName(pngPath_) + ".jpg"
        ),
        quality=95
    )


# 判断给定路径的图片内的大小，宽高中最大或最小进行比较（isMaxCompare_=True 用最大的比较）
def resizePic(picPath_, triggleSize_=4096, isMaxCompare_=False):
    if picPath_.lower().endswith(".jpg") or picPath_.lower().endswith(".jpeg"):
        _picType = 'jpeg'
    elif picPath_.lower().endswith(".png"):
        _picType = 'png'
    elif picPath_.lower().endswith(".tif") or picPath_.lower().endswith(".tiff"):
        _picType = 'tiff'
    else:
        print(picPath_ + " 后缀不是图片")
        sys.exit(1)
    _im = Image.open(picPath_)
    # 宽高大于一定数值，就要变更尺寸。
    _xs = 1
    if not isMaxCompare_:
        # 最小的去比
        if min(_im.width, _im.height) > triggleSize_:
            _xs = min(_im.width, _im.height) / triggleSize_
    else:
        # 最大的去比
        if max(_im.width, _im.height) > triggleSize_:
            _xs = max(_im.width, _im.height) / triggleSize_
    # 系数不是1，证明变化过
    if not _xs == 1:
        _width = int(_im.width / _xs)
        _height = int(_im.height / _xs)
        out = _im.resize((_width, _height), Image.ANTIALIAS)
        out.save(picPath_, _picType)
        print("放缩到 " + str(1 / _xs))
    else:
        print("并未放缩")


# 变换图片的尺寸
def resizePicFolder(
        picFolderPath_,  # 承载图片的文件夹
        triggleSize_=4096,  # 触发大小
        isMaxCompare_=False
):
    _fileWithSuffixList = utils.folderUtils.getFilterFilesInPath(picFolderPath_,
                                                                 [".png", ".jpg", ".jpeg", ".tif", ".tiff"])
    for _i in range(len(_fileWithSuffixList)):
        _picPath = _fileWithSuffixList[_i]
        print(str(_i + 1) + "/" + str(len(_fileWithSuffixList)) + '    ' + str(_picPath))
        resizePic(_picPath, triggleSize_, isMaxCompare_)


# 图片转换成jpg
def convertPicToJpg(
        picFolderPath_,  # 目标文件夹内的图片，转换成jpg
        suffixList_  # 指定后缀文件，转换后删除
):
    for _idx in range(len(suffixList_)):
        _fileWithSuffixList = utils.folderUtils.getFilePathWithSuffixInFolder(picFolderPath_, suffixList_[_idx])
        for _i in range(len(_fileWithSuffixList)):
            _fileWithSuffix = _fileWithSuffixList[_i]
            print(str(_i + 1) + '/' + str(len(_fileWithSuffixList)) + ' : ' + str(_fileWithSuffix))
            convertToJpg(_fileWithSuffix)
            os.remove(_fileWithSuffix)


# 将给定文件夹内的jpg图合并成一个PDF
def folderJpgToPDF(
        jpgFolderPath_,  # 承载 jpg 的文件夹
        tragetFolderPath_  # 将文件夹内的 jpg 组成pdf后，放置于哪个文件夹
):
    _jpgPathList = utils.folderUtils.getFilterFilesInPath(jpgFolderPath_, [".JPG", ".jpg", ".jpeg", ".png"])
    _jpgPathList.sort()  # 排序
    _imgForPdf = Image.open(_jpgPathList[0])  # 第一张图
    _jpgPathList.pop(0)  # 推出
    _pageJpgList = []  # 其他的image
    for _jpgPath in _jpgPathList:
        _pageJpg = Image.open(_jpgPath)
        _pageJpgList.append(_pageJpg)
    _pdfName = os.path.dirname(jpgFolderPath_) + ".pdf"  # PDF 名称
    _taregtPdfPath = os.path.join(tragetFolderPath_, _pdfName)  # PDF 生成路径
    _imgForPdf.save(_taregtPdfPath, "PDF", resolution=100.0, save_all=True, append_images=_pageJpgList)
    print("生成 pdf : ", _taregtPdfPath)


# 拆分图片
def splitPicInFolder(picFolderPath_, colNum_, lineNum_):
    # 可以进行超大图片操作
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    Image.MAX_IMAGE_PIXELS = None
    print('split : ' + str(picFolderPath_))
    _fileWithSuffixList = utils.folderUtils.getFilterFilesInPath(picFolderPath_, [".jpg", ".jpeg"])
    for _i in range(len(_fileWithSuffixList)):
        _picPath = _fileWithSuffixList[_i]
        _prefix = _picPath.split('.')[0]
        _suffix = _picPath.split('.')[1]
        _count = 0
        _im = Image.open(_picPath)
        _width = math.floor(_im.width / colNum_)
        _height = math.floor(_im.height / lineNum_)
        for _lineIdx in range(0, lineNum_):
            for _colIdx in range(0, colNum_):
                _count += 1
                _box = (_colIdx * _width, _lineIdx * _height, (_colIdx + 1) * _width, (_lineIdx + 1) * _height)
                _picNewName = _prefix + "_<" + str(_count) + ">." + _suffix
                _imSplit = _im.crop(_box)
                _imSplit.save(_picNewName, "jpeg")
        os.remove(_picPath)


# 图片列表 按照 行列数 合并
def contactPics(filePath_, imList_, column_, line_):
    _lineImList = []  # 成行图片列表
    for _lineIdx in range(0, line_):
        _colImList = []
        for _colIdx in range(0, column_):
            _colImList.append(imList_[_lineIdx * column_ + _colIdx])
        _lineImList.append(contactPicsH(_colImList))
    contactPicsV(_lineImList).save(filePath_, "jpeg")


# 竖方向合并图片
def contactPicsV(imList_):
    _targetWidth = 0
    for _i in range(len(imList_)):
        _im = imList_[_i]
        if _im.width > _targetWidth:
            _targetWidth = _im.width
    _targetHeight = 0
    for _i in range(len(imList_)):
        _im = imList_[_i]
        if _im.width != _targetWidth:
            _currentTargetHeight = int(_im.height * _targetWidth / _im.width)
            imList_[_i] = _im.resize((_targetWidth, _currentTargetHeight), Image.ANTIALIAS)
            _targetHeight = _targetHeight + _currentTargetHeight
        else:
            _targetHeight = _targetHeight + _im.height
    result = Image.new(imList_[0].mode, (_targetWidth, _targetHeight))
    _targetHeight = 0
    for _i in range(len(imList_)):
        _im = imList_[_i]
        result.paste(_im, box=(0, _targetHeight))
        if _im.width != _targetWidth:
            _currentTargetHeight = int(_im.height * _targetWidth / _im.width)
            _targetHeight = _targetHeight + _currentTargetHeight
        else:
            _targetHeight = _targetHeight + _im.height
    return result


# 横向合并图片
def contactPicsH(imList_):
    # 算最大搞
    _targetHeight = 0
    for _i in range(len(imList_)):
        _im = imList_[_i]
        if _im.height > _targetHeight:
            _targetHeight = _im.height
    # 调整大小
    _targetWidth = 0
    for _i in range(len(imList_)):
        _im = imList_[_i]
        if _im.height != _targetHeight:
            _currentTargetWidth = int(_im.width * _targetHeight / _im.height)
            imList_[_i] = _im.resize((_currentTargetWidth, _targetHeight), Image.ANTIALIAS)
            _targetWidth = _targetWidth + _currentTargetWidth
        else:
            _targetWidth = _targetWidth + _im.width
    # 目标图
    result = Image.new(imList_[0].mode, (_targetWidth, _targetHeight))
    # 绘制
    _targetWidth = 0
    for _i in range(len(imList_)):
        _im = imList_[_i]
        result.paste(_im, box=(_targetWidth, 0))
        if _im.height != _targetHeight:
            _currentTargetWidth = int(_im.width * _targetHeight / _im.height)
            _targetWidth = _targetWidth + _currentTargetWidth
        else:
            _targetWidth = _targetWidth + _im.width
    return result


# 转换成黑白图
def convertJpgToBlackWhite(
        jpgFolderPath_,  # 承载 jpg 的文件夹
        targetFolderPath_  # 转换成黑白图之后，将其放置于哪个文件夹
):
    _jpgPathList = utils.folderUtils.getFilePathWithSuffixInFolder(jpgFolderPath_, ".jpg")
    utils.folderUtils.makeSureDirIsExists(targetFolderPath_)
    for _jpgPath in _jpgPathList:
        _jpgImg = Image.open(_jpgPath)
        _jpgImg = _jpgImg.convert("L")  # 转化为黑白图片
        _jpgImg.save(os.path.join(targetFolderPath_, os.path.basename(_jpgPath)))


# 删除 满足条件的 文件
def remove(picFolderPath_):
    _fileWithSuffixList = utils.folderUtils.getFilterFilesInPath(picFolderPath_, [".jpg", ".jpeg"])
    _fileWithSuffixList.sort()

    for _i in range(len(_fileWithSuffixList)):
        _filePath = _fileWithSuffixList[_i]
        # 条件在这里写
        if _filePath.endswith(" 2.jpg"):
            utils.fileUtils.removeExistFile(_filePath)


# 按比例，保留居中部分
def cutFrame(picFolderPath_):
    _xsX = 0.75
    _xsY = 0.786
    _fileWithSuffixList = utils.folderUtils.getFilterFilesInPath(picFolderPath_, [".jpg", ".jpeg"])
    _fileWithSuffixList.sort()
    for _i in range(len(_fileWithSuffixList)):
        _picPath = _fileWithSuffixList[_i]
        _imSrc = Image.open(_picPath)
        os.remove(_picPath)
        _width = _imSrc.width
        _height = _imSrc.height
        _xsBufferX = (1 - _xsX) * 0.5
        _xsBufferY = (1 - _xsY) * 0.5
        _box = (
            _xsBufferX * _width, _xsBufferY * _height, _width * (_xsX + _xsBufferX), _height * (_xsY + _xsBufferY)
        )
        _image = _imSrc.crop(_box)
        _image.save(_picPath, "jpeg")


# 根据文件夹内的图片个数，自动选取一个合适的矩阵数，进行合并，生成一张大图
def contactPicInFolderAuto(picFolderPath_, column_=None, line_=None):
    _fileWithSuffixList = utils.folderUtils.getFilterFilesInPath(picFolderPath_, [".jpg", ".jpeg", ".Jpeg"])
    _fileWithSuffixList.sort()
    _length = len(_fileWithSuffixList)

    if column_ is not None and line_ is not None and _length % (column_ * line_) != 0:
        print('个数不对 : ' + str(_length) + " - " + str(column_) + " x " + str(line_))
        return False

    _setColAndLine = False
    if (column_ is None) and (line_ is None):
        _column, _line = utils.numUtils.getColLineNum(_length)  # 获取 分割方式
        if _column == 0:
            print(picFolderPath_ + ' 文件数 : ' + str(_length) + " 数字分割不支持")
            return False
    else:
        _setColAndLine = True
        _column, _line = column_, line_

    # 每一段的个数
    _segmentNum = _column * _line
    _picDict = {}
    _imList = None
    for _i in range(_length):
        _picPath = _fileWithSuffixList[_i]
        if _i % _segmentNum == 0:  # 记录一组的起始路径
            _imList = []
            _picDict[_picPath] = _imList
        _im = Image.open(_picPath)  # 读取图片内容
        if not _setColAndLine and _i == 0:
            if _im.width > _im.height:  # 判断一下宽高
                _line, _column = _column, _line  # 决定摆放的方向
        _imList.append(_im)  # 缓存图片内容
        os.remove(_picPath)  # 删除原始图片

    # 键值对
    for _picPath in _picDict:
        _imList = _picDict[_picPath]
        contactPics(_picPath, _imList, _column, _line)
    return True


# 将文件夹内的文件统一放缩
def scale(folder_, scale_):
    for _fileName in os.listdir(folder_):
        if not _fileName.endswith('.jpg') and not _fileName.endswith('.jpeg'):
            continue
        _im = Image.open(os.path.join(folder_, _fileName))
        _width, _height = _im.size
        _im.thumbnail((_width * scale_, _height * scale_))
        _im.save(folder_ + '/' + _fileName, 'jpeg')


# 文件夹内图片自动合并
def folderAutoContact(parentFolderPath_):
    _folderPathList = utils.folderUtils.getFolderNameListJustOneDepth(parentFolderPath_)
    # 生成图片
    for _idx in range(len(_folderPathList)):
        _folderPath = os.path.join(parentFolderPath_, _folderPathList[_idx])
        # 个数满足自动条件就可以合成
        if contactPicInFolderAuto(_folderPath):
            # 将成功执行的结果拷贝到文件夹上层（清空文件夹）。
            _fileWithSuffixList = utils.folderUtils.getFilterFilesInPath(_folderPath, [".jpg", ".jpeg", ".Jpeg"])
            for _idxInside in range(len(_fileWithSuffixList)):
                _filePath = _fileWithSuffixList[_idxInside]  # 生成的图片，移到最外层
                shutil.move(
                    _filePath,
                    parentFolderPath_ + _filePath.split(_folderPath)[1]
                )
    # 删除空文件夹
    utils.folderUtils.deleteEmptyFolder(parentFolderPath_)


# 根据图片的大小将图片分散到各个文件夹。相同大小的放到同一个文件夹
def separateToFolderBySize(folderPath_: str, targetFolderPath_: str):
    _fileWithSuffixList = utils.folderUtils.getFilterFilesInPath(folderPath_, [".jpg", ".jpeg", ".Jpeg"])
    _sizeSubFolderPathDict = {}
    for _i in range(len(_fileWithSuffixList)):
        _filePath = _fileWithSuffixList[_i]
        _im = Image.open(_filePath)  # 读取图片内容
        _sizeKey = str(_im.width) + "_" + str(_im.height)  # 大小拼接键
        if not (_sizeKey in _sizeSubFolderPathDict):
            _sizeSubFolderPathDict[_sizeKey] = os.path.join(targetFolderPath_, _sizeKey)
        _targetFolderPath = _sizeSubFolderPathDict[_sizeKey]  # 键映射目标路径
        utils.folderUtils.makeSureDirIsExists(_targetFolderPath)  # 确保目标路径存在
        _targetFilePath = os.path.join(_targetFolderPath, os.path.basename(_filePath))
        shutil.copy(_filePath, _targetFilePath)  # 将文件移动到对应大小的目录
        print(_filePath + ' -> ' + _targetFilePath)


# 将剪切板内的图片，剪切到同一目录，并将目录剪贴到给定目录中。
def useClipBoardPicsCreateFolder(targetFolderPath_: str):
    _clipPicPathList = utils.sysUtils.getClipBoardPathList([".JPG", ".JPEG", ".PNG"])
    # 空表示出错，不在再继续进行
    if not _clipPicPathList:
        return
    # 目标文件夹名称由第一张图片决定
    _targetFolderName = utils.fileUtils.justName(_clipPicPathList[0])
    # 目标文件夹路径
    _targetFolderPath = os.path.join(targetFolderPath_, _targetFolderName)
    # 剪切关系字典
    _fromToDict = {}
    for _i in range(len(_clipPicPathList)):
        _fromPicPath = _clipPicPathList[_i]
        _picName = os.path.basename(_fromPicPath)
        _toPicPath = os.path.join(_targetFolderPath, _picName)
        _fromToDict[_fromPicPath] = _toPicPath  # 构建剪切关系
    # 创建文件夹，剪切文件
    utils.folderUtils.makeSureDirIsExists(_targetFolderPath)
    for _fromPicPath in _fromToDict:
        _toPicPath = _fromToDict[_fromPicPath]
        print(str(_fromPicPath) + ' -> ' + str(_toPicPath))
        shutil.move(_fromPicPath, _toPicPath)


# 横向翻转
def flipH(picFilePath_: str):
    _img = cv2.imread(picFilePath_)
    _horizontalFlipImg = cv2.flip(_img, 1)
    cv2.imwrite(picFilePath_, _horizontalFlipImg)


# 给定目录中递归层级，将所含图片都拿出来放到目录根处，删除空文件夹。
def bubbleMovePicThenDeleteEmptyFolder(folderPath_: str):
    _fileNameToPathDict = utils.folderUtils.getFilePathKeyValue(folderPath_, [".jpg", ".png", ".jpeg"])
    for _fileName in _fileNameToPathDict:
        _filePath = _fileNameToPathDict[_fileName]
        _toFilePath = os.path.join(folderPath_, os.path.basename(_filePath))
        shutil.move(_filePath, _toFilePath)
    # 删除空文件夹
    utils.folderUtils.deleteEmptyFolder(folderPath_)


if __name__ == "__main__":
    # # 图片左右翻转
    # flipH("/Users/nobody/Documents/picUse/folder/035_043_014/521_348_328的副本.jpg")
    # sys.exit(1)

    # # 剪切板图片整合成文件夹，移动到指定文件夹内
    # useClipBoardPicsCreateFolder("/Users/nobody/Documents/picUse/subFolder/")
    # sys.exit(1)

    # # 图片都挪到目录根处，删除空文件夹
    # bubbleMovePicThenDeleteEmptyFolder("/Users/nobody/Documents/picUse/sizeFolder/")
    # sys.exit(1)

    # # 删除 A 目录中，已经存在于 B 目录中的同名文件
    # utils.folderUtils.removeAFilesInB(
    #   "/Users/nobody/Documents/picUse/recover/",
    #   "/Users/nobody/Documents/picUse/contact/",
    #   [".jpg", ".jpeg"]
    # )
    # scale("/Users/nobody/Documents/picUse/split/", 0.555)

    # # 按照指定行列数，拆分图片
    # splitPicInFolder("/Users/nobody/Documents/picUse/contact/", 2, 1)
    # sys.exit(1)

    # 将目录中的图片按照大小分别放入各自文件夹
    # separateToFolderBySize("/Users/nobody/Documents/picUse/contact/", "/Users/nobody/Documents/picUse/folder/")
    # sys.exit(1)

    # # 其中每一个文件夹都自动合并成图。
    # folderAutoContact("/Users/nobody/Documents/picUse/subFolder/")
    # sys.exit(1)

    # # 将名称中匹配到的第二项作为数字，修改其格式，使得文件夹内的名称可以正常排序。
    # utils.folderUtils.renameNum("/Users/nobody/Documents/picUse/contact/",
    #                             # r'(.*?)([0-9]+)_(.*)_.*'
    #                             r'(IMG \()([0-9]+)(.*)'
    #                             )

    # # 按照指定行列合并
    # contactPicInFolderAuto("/Users/nobody/Documents/picUse/contact/", 2, 2)
    # sys.exit(1)

    # 交换相邻两张图片
    # utils.folderUtils.switchNearByFileNames("/Users/nobody/Documents/picUse/contact/")

    # 改变图片大小
    # resizePicFolder("/Users/nobody/Documents/picUse/contact/", 2000, True)

    # 裁切边框
    # cutFrame("/Users/nobody/Documents/picUse/cut/")

    # 图片转换成jpg
    # _pngfolderPath = "/Volumes/Files/Downloads/伯里曼/"
    # convertPicToJpg(_pngfolderPath, [".bmp", ".png", ".tif", ".tiff"])

    # 把一个文件夹内的图片变成一个PDF
    # folderJpgToPDF(
    #     "/Users/nobody/Documents/picUse/pdf/"
    #     ,
    #     "/Users/nobody/Documents/picUse/Unity_UniversalRP_内置Shader解析"
    # )

    # _fileWithSuffixList = utils.folderUtils.getFilePathWithSuffixInFolder(_pngfolderPath, ".png")
    # for _i in range(len(_fileWithSuffixList)):
    #     _fileWithSuffix = _fileWithSuffixList[_i]
    #     print(str(_i + 1) + '/' + str(len(_fileWithSuffixList)) + ' : ' + str(_fileWithSuffix))
    #     convertToJpg(_fileWithSuffix)
    #     os.remove(_fileWithSuffix)

    # _fileWithSuffixList = utils.folderUtils.getFilePathWithSuffixInFolder(_pngfolderPath, ".bmp")
    # for _i in range(len(_fileWithSuffixList)):
    #     _fileWithSuffix = _fileWithSuffixList[_i]
    #     print(str(_i + 1) + '/' + str(len(_fileWithSuffixList)) + ' : ' + str(_fileWithSuffix))
    #     convertToJpg(_fileWithSuffix)
    #     os.remove(_fileWithSuffix)

    print(1)
