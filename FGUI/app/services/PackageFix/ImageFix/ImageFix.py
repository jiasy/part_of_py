#!/usr/bin/env python3
# Created by nobody at 2023/7/18
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import xmlUtils
from FGUI.fguiUtils import fguiUtils


class ImageFix(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        # 发现需要修复的图片ID时，记录从哪个 src 修复到 哪个 Id
        self.imageFixFromSrc = None
        self.imageFixToId = None

    def create(self):
        super(ImageFix, self).create()

    def destroy(self):
        super(ImageFix, self).destroy()

    # 每一个 image 进行判断，直到找到 src 和当前要修改的图片一致的那张图
    def fixImage(self, imageDict_: dict):
        if imageDict_["@src"] == self.imageFixFromSrc:
            imageDict_["@src"] = self.imageFixToId
            self.imageFixFromSrc = None
            self.imageFixToId = None
            return imageDict_
        return None

    def fixLostImageSingle(self, xmlPath_: str, imageDict_: dict, packageXmlDict_: dict):
        if "@pkg" not in imageDict_:  # 不是外部引用
            if '@fileName' in imageDict_:  # 使用了图片
                _fileName = imageDict_['@fileName']
                # 删

    # 修复包内丢失引用的图片，引用自己包内的图。
    def fixLostImageInPackage(self, xmlPath_: str, xmlContentDict_: dict, packageXmlDict_: dict):
        _imageList = fguiUtils.getImageListFromComponent(xmlContentDict_)
        for _i in range(len(_imageList)):
            _imgDict = _imageList[_i]
            self.fixLostImageSingle(xmlPath_, _imgDict, packageXmlDict_)


# 获取自己对应的资源
# self.tempFile = fileUtils.getPath(self.resPath, self.className + ".suffix")

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
