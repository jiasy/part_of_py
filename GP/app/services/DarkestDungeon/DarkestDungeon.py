#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from utils import folderUtils
from utils import fileUtils
from utils import jsonUtils
from utils import printUtils
from utils.infoUtils.InfoColor import InfoColor
import sys

from utils import fileCopyUtils
import os
import json
from utils import cmdUtils

# 创意工坊路径
_workShopFolder = "/Volumes/things/SteamLibrary/steamapps/workshop/content/262060"
# 动画名称
_actNameList = [
    "afflicted",
    # "atack_lash",
    # "attack_deathless",
    # "attack_more",
    # "attack_punish",
    # "attack_rain",
    # "attack_sepsis",
    "camp",
    "combat",
    "defend",
    "idle",
    "investigate",
    "walk",
]
# spine 还原工具
from Spine.app.services.SpineReverse import SpineReverse

_spineFileCopy: SpineReverse = pyServiceUtils.getSvrByName("Spine", "SpineReverse")


class DarkestDungeon(BaseService):
    def __idxnit__(self, sm_):
        super().__idxnit__(sm_)

    def create(self):
        super(DarkestDungeon, self).create()

    def destroy(self):
        super(DarkestDungeon, self).destroy()

    # 修改价格
    def dealPrice(self, entries_trinkets_filePath_, rarityRecordList_):
        _jsonDict = fileUtils.dictFromJsonFile(entries_trinkets_filePath_)
        if "entries" in _jsonDict:
            _entries = _jsonDict["entries"]
            for _idx in range(len(_entries)):
                _entry = _entries[_idx]
                # 饰品售价
                if "price" in _entry:
                    _price = _entry["price"]
                    print('_price = ' + str(_price))
                    _entry["price"] = 1
                else:
                    if not "shard" in _entry:
                        print('无售卖价格，非售卖')
                # 统计饰品类别综述
                if "rarity" in _entry:
                    _rarity = _entry["rarity"]
                    if _rarity not in rarityRecordList_:
                        rarityRecordList_.append(_rarity)
            fileUtils.writeFileWithStr(entries_trinkets_filePath_, str(json.dumps(_jsonDict, indent=4, sort_keys=False, ensure_ascii=False)))

    # 修改 buff
    def dealBuff(self, buffs_filePath_):
        _jsonDict = fileUtils.dictFromJsonFile(buffs_filePath_)
        if "buffs" in _jsonDict:
            _buffs = _jsonDict["buffs"]
            _has = False
            for _idx in range(len(_buffs)):
                _buff = _buffs[_idx]
                if "stat_type" in _buff:
                    # 压力伤害 食物消耗 大于 0 就翻转
                    if _buff["stat_type"] == "stress_dmg_received_percent" or _buff["stat_type"] == "food_consumption_percent":
                        if "amount" in _buff and _buff["amount"] > 0:
                            _buff["amount"] = -1 * _buff["amount"]
                            _has = True
                    # 致死抗性
                    if _buff["stat_type"] == "resistance" and _buff["stat_sub_type"] == "death_blow":
                        if "amount" in _buff and _buff["amount"] < 0:
                            _buff["amount"] = -1 * _buff["amount"]
                            _has = True
            if _has:
                fileUtils.writeFileWithStr(buffs_filePath_, str(json.dumps(_jsonDict, indent=4, sort_keys=False, ensure_ascii=False)))
                print('buffs_filePath_ = ' + str(buffs_filePath_))

    # work Shop 中的内容修改
    def forEachJson(self):
        _rarityRecordList = []
        _jsonFileList = folderUtils.getFileListInFolder(_workShopFolder, [".json"])
        for _idxdx in range(len(_jsonFileList)):
            _jsonFile = _jsonFileList[_idxdx]
            # 饰品价格
            if str(_jsonFile).endswith("entries.trinkets.json"):
                # self.dealPrice(_jsonFile, _rarityRecordList)
                continue
            # 饰品效果
            if str(_jsonFile).endswith("buffs.json"):
                self.dealBuff(_jsonFile)

        # 饰品 类别综述
        printUtils.printList(_rarityRecordList, "_rarityRecordList")

    # spine 文件拷贝
    def heroSpineFilesCopy(self):
        _heroSpineReverseContainer = os.path.join(self.resPath, "heroSpine")
        _folderNameList = folderUtils.getFolderNameListJustOneDepth(_workShopFolder)
        for _idx in range(len(_folderNameList)):
            _folderPath = os.path.join(_workShopFolder, _folderNameList[_idx])
            # 存在英雄的相关改动
            _heroesFolderPath = os.path.join(_folderPath, "heroes")
            _hasError = False
            if os.path.exists(_heroesFolderPath):
                _heroNameList = folderUtils.getFolderNameListJustOneDepth(_heroesFolderPath)  # 改动的每个英雄
                for _heroLoopIdx in range(len(_heroNameList)):
                    _hasError = False
                    _heroName = _heroNameList[_heroLoopIdx]
                    _heroFolderPath = os.path.join(_heroesFolderPath, _heroName)
                    print(f"{_heroName} - {_heroFolderPath}")
                    # 存在英雄动画
                    _heroAnimFolderPath = os.path.join(_heroFolderPath, "anim")
                    if os.path.exists(_heroAnimFolderPath):
                        _heroPngFolderPath = os.path.join(_heroFolderPath, f"{_heroName}_A")  # 存在 A 皮肤
                        if not os.path.exists(_heroPngFolderPath):
                            print(f"ERROR - - - 1 --- {_heroName}")
                        else:
                            for _i in range(len(_actNameList)):  # 遍历每一个动作
                                _actName = _actNameList[_i]
                                _heroSpineName = f"{_heroName}.sprite.{_actName}"
                                _heroPngFilePath = os.path.join(_heroPngFolderPath, "anim", f"{_heroSpineName}.png")
                                if not os.path.exists(_heroPngFilePath):
                                    print(f"ERROR  - - - 2 --- {_actName}")
                                else:
                                    # 这个动作下的各个英雄的文件拷贝
                                    _heroSpineReverseFolder = os.path.join(_heroSpineReverseContainer, _actName)
                                    folderUtils.makeSureDirIsExists(_heroSpineReverseFolder)
                                    # 没整理过文件的话，这里指的是拷贝后执行脚本会把 png + skel + atlas 都放到的那个文件夹
                                    if not os.path.exists(os.path.join(_heroSpineReverseFolder, _heroSpineName)):
                                        # 源路径
                                        _heroSkelFilePath = os.path.join(_heroAnimFolderPath, f"{_heroSpineName}.skel")
                                        _heroAtlasFilePath = os.path.join(_heroAnimFolderPath, f"{_heroSpineName}.atlas")
                                        # 目标文件路径
                                        fileCopyUtils.copyFile(_heroPngFilePath, os.path.join(_heroSpineReverseFolder, f"{_heroSpineName}.png"))
                                        fileCopyUtils.copyFile(_heroSkelFilePath, os.path.join(_heroSpineReverseFolder, f"{_heroSpineName}.skel"))
                                        fileCopyUtils.copyFile(_heroAtlasFilePath, os.path.join(_heroSpineReverseFolder, f"{_heroSpineName}.atlas"))

    def spineCmd_00(self):
        _heroSpineReverseContainer = os.path.join(self.resPath, "heroSpine")
        # 整理刚拷贝的动画文件
        for _i in range(len(_actNameList)):  # 遍历每一个动作
            _actName = _actNameList[_i]
            _heroSpineReverseFolder = os.path.join(_heroSpineReverseContainer, _actName)
            # 拷贝并执行工具，可能新添加了动作
            _shToolSrc = os.path.join(_spineFileCopy.resPath, "Tools", "spine还原批处理mac", "00_整理文件_zlp.sh")
            _shToolDst = os.path.join(_heroSpineReverseFolder, "00_整理文件_zlp.sh")
            fileCopyUtils.copyFile(_shToolSrc, _shToolDst)
            cmdUtils.doStrAsCmd(f"sh {_shToolDst}", _heroSpineReverseFolder)

    def spineCmd_01(self):
        self.fixSpineFolder()  # 去除嵌套了之后，再走流程
        _heroSpineReverseContainer = os.path.join(self.resPath, "heroSpine")
        # 整理刚拷贝的动画文件
        for _i in range(len(_actNameList)):  # 遍历每一个动作
            _actName = _actNameList[_i]
            _heroSpineReverseFolder = os.path.join(_heroSpineReverseContainer, _actName)
            # 拷贝解png的脚本
            _shToolSrc = os.path.join(_spineFileCopy.resPath, "Tools", "spine还原批处理mac", "01_atlas纹理解包_zlp.sh")
            _shToolDst = os.path.join(_heroSpineReverseFolder, "01_atlas纹理解包_zlp.sh")
            fileCopyUtils.copyFile(_shToolSrc, _shToolDst)
            cmdUtils.doStrAsCmd(f"sh {_shToolDst}", _heroSpineReverseFolder)

    def fixSpineFolder(self):
        _heroSpineReverseContainer = os.path.join(self.resPath, "heroSpine")
        # 多次执行脚本会嵌套文件夹，将嵌套的文件夹去除
        for _i in range(len(_actNameList)):  # 遍历每一个动作
            _actName = _actNameList[_i]
            _heroSpineReverseFolder = os.path.join(_heroSpineReverseContainer, _actName)
            _heroSpineNameList = folderUtils.getFolderNameListJustOneDepth(_heroSpineReverseFolder)  #
            for _idx in range(len(_heroSpineNameList)):
                _heroSpineName = _heroSpineNameList[_idx]
                _rootHeroSpineFolder = os.path.join(_heroSpineReverseFolder, _heroSpineName)
                _currentFolder = _rootHeroSpineFolder
                while os.path.exists(os.path.join(_currentFolder, _heroSpineName)):
                    _currentFolder = os.path.join(_currentFolder, _heroSpineName)
                if _currentFolder != _rootHeroSpineFolder:  # 发生嵌套
                    # 内容拷贝出来
                    fileCopyUtils.copyFile(os.path.join(_currentFolder, f"{_heroSpineName}.png"), os.path.join(_rootHeroSpineFolder, f"{_heroSpineName}.png"))
                    fileCopyUtils.copyFile(os.path.join(_currentFolder, f"{_heroSpineName}.skel"), os.path.join(_rootHeroSpineFolder, f"{_heroSpineName}.skel"))
                    fileCopyUtils.copyFile(os.path.join(_currentFolder, f"{_heroSpineName}.atlas"), os.path.join(_rootHeroSpineFolder, f"{_heroSpineName}.atlas"))
                    # 删除嵌套的第一层
                    folderUtils.removeTree(os.path.join(_rootHeroSpineFolder, _heroSpineName))


if __name__ == '__main__':
    _darkestDungeon: DarkestDungeon = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_darkestDungeon.resPath))
    pyServiceUtils.printSvrCode(__file__)

    # 修改数值
    # _darkestDungeon.forEachJson()

    # 提取Spine
    # _darkestDungeon.heroSpineFilesCopy()
    # _darkestDungeon.spineCmd_00()
    _darkestDungeon.spineCmd_01()
