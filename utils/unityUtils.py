from utils import folderUtils
from utils import listUtils
from utils import sysUtils
import yaml
import os
import utils.printUtils

'''
文本类
    .xml
    .txt
    .plist
    .yml
    .json
    .md
    .proto
    .dat (DATA 数据文件，内容自定，加解密自定)
    .data (DATA 数据文件，内容自定，加解密自定)
    .pdf
    .xls
    .info (描述，直接文本文件打开即可)
    .rtf (Rich Text Format)
数据库
    .mdb (Office ACCESS)
    .db (数据库文件)
    .pdb (数据库文件)
工程类
    .csproj
    .pbxproj
    .xsd(XML Schema Definition,XML模式定义 VisualStudio 用)
日之类
    .buildreport
    .log
脚本类
    .html
    .py
    .sh
    .bat
    .cs
    .pch ( 预编译头文件,是把一个工程中较稳定的代码预先编译好放在一个文件里)
    .h
    .cpp
    .c
    .mm
    .m
    .lua
    .scss (CSS的拓展，在浏览器运行时转换回CSS)
编译库
    .o
    .so
    .dll
    .a
    .jar
    .stamp (编译进程记录文件，删除相应模块可能重编译)
Unity-Editor
    .asmdef
    .meta
    .config
    .controller
    .anim
    .fontsettings
    .renderTexture
    .prefab    
    .physicsMaterial2D
    .spriteatlas
    .shadervariants
    .unitypackage
    .assets
    .resource
    .unity
    .asset
    .mat
    .cube
    .uxml (Unity XML,界面排布文本)
    .guiskin (Unity GUI 自定义风格)
美术资源
    .tga
    .png
    .jpg
    .ttf (TrueTypeFont,Apple + Microsoft 共同推出的字体文件)
    .tiff (Tag Image File Format)
    .fnt
    .otf (OpenType Font 该OTF文件扩展名是最初开发由微软随后被Adobe收购的字体文件类型)
    .spine
    .fbx
    .dds (DirectDraw Surface，DirectX纹理)
    .obj (Alias|Wavefront 公司为3D建模和动画软件 "Advanced Visualizer"开发的一种标准)
    .exr (OpenEXR是由工业光魔（Industrial Light & Magic）开发的一种HDR标)
    .hdr (HDRI(High-Dynamic Range Image)就是记录采用了HDR技术的图象数据文件)
美术源文件
    .psd
SHADER
    .hlsl
    .shader
    .compute
    .cginc
音效
    .mp4
    .ogg    
    .wav
    .mp3
    .aiff (Audio Interchange File Format,音频文件)
    .bank (旁白音效)
秘钥、证书
    .p12
    .mobileprovision
安卓
    .gradle
    .properties
    .manifest
    .aar
    .keystore
    .prefs
IOS
    .storyboard (界面编辑文件)
    .strings (IOS,显示文字-多国语言)
        InfoPlist.strings	App 系统显示层面上的本地化的（如 App 名字）
        Localizable.strings	代码中用到的字符串用宏 NSLocalizedString(key, comment) 做本地化默认 .strings 文件
        xxx.strings	自定义本地化文件，用宏 NSLocalizedStringFromTable(key, tbl, comment)来指定 .strings 文件的来源
压缩
    .zip
    .car
二进制
    .bytes
    .bin (binary,二进制文件)

    .cache (缓存文件)
------------------
    .dwlt
    .modulemap (DEFINES_MODULE,swift和C混编)Y
    .uss
    .guid
    .sln
    .ab
    .all
    .idx
    .pack
    .bc
    .preset
    .SYMDEF
'''


# 获取关系字典
def getIdToPathDicts(assetsPath_, filters_=None):
    _filters = filters_
    if not _filters:
        _filters = [".png", ".jpg", ".mat", ".prefab", ".controller", ".anim", ".FBX", ".PNG", ".physicsMaterial2D"]

    _filePathList = folderUtils.getFileListInFolder(
        assetsPath_,
        _filters
    )
    _guidToPathdict = {}
    _relativePathToIdDict = {}
    for _i in range(len(_filePathList)):
        _filePath = _filePathList[_i]
        _metaFilePath = _filePath + ".meta"
        _fs = open(_metaFilePath, encoding="UTF-8")
        _yamlData = yaml.load(_fs, Loader=yaml.FullLoader)
        _relativePath = _filePath.split(assetsPath_)[1]
        _relativePathToIdDict[_relativePath] = _yamlData["guid"]
        _guidToPathdict[_yamlData["guid"]] = _relativePath
    return _guidToPathdict, _relativePathToIdDict


class SubUnityYaml:
    def __init__(self, path_: str, fileId_: str, content_: str):
        self.path = path_
        self.fileId = fileId_
        self.yamlDict = None  # 内容对象
        self.type = None  # 应当只有一个键值对，键是类型，值是对象。
        self.parse(content_)  # 解析内容

    # 内容转换成字典
    def parse(self, content_: str):
        _yamlDict = yaml.load(content_, Loader=yaml.FullLoader)  # 转换成对象
        _keyCount = 0
        for _key in _yamlDict:
            _keyCount += 1
            if _keyCount > 1:
                print("Unity 的yaml文件，内容切割成多个 yaml 后，每一个 yaml 结构中，只能有一个键\n")
                return False
            self.type = _key
        self.yamlDict = _yamlDict[self.type]
        return True


class UnityYaml:
    def __init__(self, path_):
        self.fileIdToSubYamlDict = {}
        self.path = path_
        self.parse(path_)

    # 解开指定路径内容
    def parse(self, path_: str):
        _yamlLinesDict = {}  # fileID对应的行
        _fileId = None
        with open(path_, 'r') as _file:
            for _line in _file:
                if _line.startswith('---'):  # ---是 yaml 的内部分割符号，下一行开始就是一个yaml文件
                    _fileId = _line.split(" &")[1].split("\n")[0]  # 记录 fileID
                    _yamlLinesDict[_fileId] = []
                else:
                    if _fileId is not None:  # 大于等于零时，证明文件已经开始切割
                        _yamlLinesDict[_fileId].append(_line)
        # 每一个 fileId 对应的内容
        for _fileId in _yamlLinesDict:
            self.fileIdToSubYamlDict[_fileId] = SubUnityYaml(
                path_,
                _fileId,
                listUtils.joinToStr(_yamlLinesDict[_fileId], "")
            )

    # 通过类型获取子项列表
    def getSubYamlsByType(self, type_: str):
        _list = []
        for _key in self.fileIdToSubYamlDict:
            _subYamlDict = self.fileIdToSubYamlDict[_key]
            if _subYamlDict.type == type_:
                _list.append(_subYamlDict)
        if len(_list) > 0:
            return _list
        else:
            return None

    # 通过fileId获取子对象
    def geSubYamlByFileId(self, fileId_: str):
        if fileId_ not in self.fileIdToSubYamlDict:
            fileId_ = str(fileId_)
        return self.fileIdToSubYamlDict[fileId_]


class UnityProject:
    def __init__(self, assetPath_: str, filters_: list = None):
        self.assetPath = sysUtils.folderPathFixEnd(assetPath_)
        print("获取 相对路径 和 ID 的关系")
        self.guidToPathDict, self.relativePathToIdDict = getIdToPathDicts(self.assetPath, filters_)
        print("获取 ID 和 内容对象 的关系")
        self.guidToYamlDict = {}
        self.suffixToYamlListDict = {}

    # 解析某一类型后缀
    def analyseBySuffix(self, suffix_: str):
        print("类型 和 文件列表 关系")
        suffix_ = suffix_.upper()
        if suffix_ in self.suffixToYamlListDict:
            print(suffix_ + " 已经有了解析，如要添加此类型，请调用 analyseByFileList")
            return
        _count = 0
        self.suffixToYamlListDict[suffix_] = []
        for _relativePath in self.relativePathToIdDict:
            _currentSuffix = os.path.splitext(_relativePath)[1].upper()  # 取后缀
            if _currentSuffix == suffix_:
                _unityYaml = self.addUnityYaml(_relativePath)
                _count = _count + 1
        if _count == 0:
            print(suffix_ + " 没有文件 。。。。。。。")

    # 解析指定文件
    def analyseFile(self, filePath_: str):
        print("  analysing ... " + filePath_)
        if not filePath_.startswith(self.assetPath):
            utils.printUtils.pError("ERROR : " + filePath_ + " 不在当前目录中")
        _suffix = os.path.splitext(filePath_)[1].upper()  # 取后缀
        if _suffix not in self.suffixToYamlListDict:
            self.suffixToYamlListDict[_suffix] = []
        _relativePath = filePath_.split(self.assetPath)[1]
        _unityYaml = self.addUnityYaml(_relativePath)

    # 解析 guid 对应的文件
    def analyseGuid(self, guid_: str):
        if guid_ not in self.guidToPathDict:
            utils.printUtils.pError("ERROR : " + guid_ + " 没有与其对应的文件")
            return False
        _relativePath = self.guidToPathDict[guid_]
        self.analyseFile(os.path.join(self.assetPath, _relativePath))
        return True

    # 将文件转换成对象，并进行指定关联
    def addUnityYaml(self, relativePath_: str):
        _suffix = os.path.splitext(relativePath_)[1].upper()  # 取后缀
        _unityYaml = UnityYaml(os.path.join(self.assetPath, relativePath_))  # 转对象
        _guid = self.relativePathToIdDict[relativePath_]
        if _guid in self.guidToYamlDict:
            print(relativePath_ + " 已经被解析过了")
            return self.guidToYamlDict[_guid]
        self.guidToYamlDict[_guid] = _unityYaml  # guid 对象关系
        self.suffixToYamlListDict[_suffix].append(_unityYaml)  # 后缀和对象建立关系
        return _unityYaml

    # 通过guid获取对象
    def getYamlDictByGuid(self, guid_: str):
        return self.guidToYamlDict[guid_]

    # 通过后缀获取对象列表
    def getYamlListBySuffix(self, suffix_: str):
        return self.suffixToYamlListDict[suffix_.upper()]
