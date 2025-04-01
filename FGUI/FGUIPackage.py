import random
import string
import sys

from utils import fileUtils
from utils import strUtils
from utils import xmlUtils
from utils import printUtils
from utils import jsonUtils
from utils import fileContentOperateUtils
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
import os

class FGUIPackage:
    # fguiAssetPath_ 工程资源根目录，packageName_ 包对应的文件夹
    def __init__(self, fguiAssetFolder_: str, packageName_: str = None, project_=None):
        self.project = project_
        self.assetFolder = fguiAssetFolder_
        self.pkgName = packageName_
        self.packageXmlPath = os.path.join(self.assetFolder, packageName_, "package.xml")
        self.isNew = None  # 是否新建
        self.xmlDict = None  # 内容
        self.id = None  # 包id
        self.item_id_base = None
        self.next_item_index = None
        self.imageDict = None
        self.componentDict = None
        build_id = strUtils.getRandomId()
        _xmlContentDict = None
        if os.path.exists(self.packageXmlPath):
            _xmlContent = fileUtils.readFromFile(self.packageXmlPath)
            _xmlContentDict = bf.data(fromstring(_xmlContent))
        if _xmlContentDict is None:
            self.isNew = True  # 是新建
            self.xmlDict = getNewPackage(self.id)  # 创建一个xmlDict
            self.id = build_id[0:8]  # 生成一个新的ID
            printUtils.pWarn(f'new : {packageName_} -> {self.id}')
        else:
            self.isNew = False  # 不是新建
            self.xmlDict = _xmlContentDict  # 获取当前的 xmlDict
            self.id = self.xmlDict["packageDescription"]["@id"]  # 获取当前的ID
            print(f'open : {packageName_} -> {self.id}')
            # printUtils.pLog(f'open : {packageName_} -> {self.id}')
        self.item_id_base = build_id[8:]
        self.next_item_index = 0
        self.imageDict, self.componentDict = getFGUIImageComponentDict(self.xmlDict)

    def get_next_item_id(self):
        result = self.item_id_base + str(hex(self.next_item_index))[2:]
        self.next_item_index += 1
        return result

    # 添加一张图
    def addImage(self, imageDict_: dict):
        _name = str(imageDict_["@name"])
        if not _name.endswith(".png"):
            print(f"ERROR : {self.packageXmlPath} 添加图片 {_name} 失败 : 图片不用 .png 结尾")
        if _name in self.imageDict:
            print(f"ERROR : {self.packageXmlPath} 添加图片 {_name} 失败 : 同名图片已存在")
        self.imageDict[_name.split(".png")[0]] = imageDict_
        jsonUtils.addFguiXmlDictToList(self.xmlDict["packageDescription"]["resources"], "image", imageDict_)

    def getImageDictById(self, id_: str):
        for _imageName in self.imageDict:
            _imageDict = self.imageDict[_imageName]
            if _imageDict["@id"] == id_:
                return _imageDict
        return None

    # 移除掉 ID 指定的内容
    def removeAssetByIdList(self, idList_: str):
        # 记录要移除的文本的路径


    # 添加一个组件，传递在 package 中的格式
    def addComponent(self, cmpInPackageDict_: dict):


    def hasComponent(self, name_: str):
        if name_ in self.componentDict:
            return True
        return False

    # 通过 Id 获取信息
    def getCmpDictById(self, cmpId_: str):
        for _key in self.componentDict:
            _cmpDict = self.componentDict[_key]
            if _cmpDict["@id"] == cmpId_:
                return _cmpDict
        return None

    # 添加一个新组件，使用文件保存的xml内容
    def newComponent(self, cmpName_: str, cmpXmlDict_: dict):


    # 保存
    def save(self):
        fileUtils.writeFileWithStr(self.packageXmlPath, xmlUtils.dictToXmlContent(self.xmlDict, False))


if __name__ == '__main__':
    from utils.CompanyUtil import Company_BB_Utils

    # package 中添加一个 component，这个 component 可能是复制出来要进行一定修改的
    fguiAssetPath = os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/project_fgui/proj/assets")
    pkgName = "HeroBag"

    xmlName = "HeroInfoStars"
    xmlPath = os.path.join(fguiAssetPath, pkgName, f"{xmlName}.xml")
    if not os.path.exists(xmlPath):
        print(f"ERROR : 不存在 {xmlPath}")
        sys.exit(1)

    # 添加一个组件
    fguiPackage = FGUIPackage(fguiAssetPath, pkgName)
    _component = {"@id": fguiPackage.get_next_item_id(), "@name": f'{xmlName}.xml', "@path": "/", "@exported": "true"}
    if fguiPackage.hasComponent(xmlName) is False:
        fguiPackage.addComponent(_component)
        fguiPackage.save()
