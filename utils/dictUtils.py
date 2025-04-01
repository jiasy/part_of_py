# !/usr/bin/env python3
import json
import sys

from utils import fileUtils
from utils import pyServiceUtils
from utils.utils_use import dictUtils_use


# 字典打印成键值对模式
# prefix_ 前缀键，dict_ 要打印的字典
def printAsKeyValue(prefix_, dict_, print_: bool = True):
    # 删


# 通过值获取键
def getKeyByValue(dict_, value_):
    for _key in dict_:
        if dict_[_key] == value_:
            return _key
    return None


# 两个Dict合并
def mergeDict(dict_a_, dict_b_):
    # 第二个字典展开，加入第一个字典形成的新字典。
    return dict(dict_a_, **dict_b_)


# 得到按照值排序的元组数组
def getKeysByValueSorted(dict_: dict, reverse_: bool = False):
    return sorted(dict_, key=lambda x: dict_[x], reverse=reverse_)


# 得到按照值字典中的键对应的值排序的键数组...
def getKeysByValuesValueSorted(dict_: dict, itemKey_: str, reverse_: bool = False):
    return sorted(dict_, key=lambda x: dict_[x][itemKey_], reverse=reverse_)


# 显示字典结构 < 字符串中不能有\n >
def printDictAsKeyValue(object_: dict, currentPath_: str, showType_: bool = False, printAsKVList_: list = None):
    # 删


# 显示字典结构 < 字符串中不能有\n >
def showDictStructure(object_, depth_: int = 0):
    # 删


# 字典结构转换成lua对象，每一个节点的赋值都清楚显示。
def createDictAsLua(object_: dict, currentPath_: str, isProtoStuct_: bool = False, luaCodeList_: list = None):
    return dictUtils_use.dict_to_lua(object_, currentPath_, isProtoStuct_, luaCodeList_)


# 内容转换为 C# 解析 Json 时，使用的 C# 结构代码
def dictToCSharpJsonSerializeCode(rootName_: str, dict_: dict):
    _, csharp_output = dictUtils_use.dict_to_serializable_class(dict_, rootName_, [rootName_])
    return csharp_output


# 结构转 BlobAsset ,C# DOTs 中数据结构
def dictToDotsBlobAssetCode(rootName_: str, dict_: dict):
    _, csharp_output = dictUtils_use.dict_to_blob_asset(dict_, rootName_, [rootName_])
    return csharp_output


# 结构转 protobuf 定义
def dictToProtobufCode(rootName_: str, dict_: dict):
    _, csharp_output = dictUtils_use.dict_to_protobuf(dict_, rootName_, [rootName_])
    return csharp_output


'''
将关系关联成字典结构，描述这个结构树
_relationList = [('a1', 'b1'), ('a1', 'b2'), ('b2', 'c1'), ('b2', 'c2'), ('b1', 'd1')]
print(buildTreedict(_relationList))
{
    'a1': {
        'b1': {
            'd1': {}
        },
        'b2': {
            'c1': {},
            'c2': {}
        }
    }
}
'''


def buildTreedict(relationList_: list[tuple[str, str]]):
    _nodeDict = {}
    _roots = set()
    for _node, _leaf in relationList_:
        if _node not in _nodeDict:
            _nodeDict[_node] = {}
        if _leaf not in _nodeDict:
            _nodeDict[_leaf] = {}
        _nodeDict[_node][_leaf] = _nodeDict[_leaf]
        _roots.discard(_leaf)
        if _node not in _nodeDict[_leaf]:
            _roots.add(_node)

    return {_root: _nodeDict[_root] for _root in _roots}


# 查找节点
def findNode(dict_: dict, targetKey_: str):
    if targetKey_ in dict_:
        return dict_[targetKey_]
    for _, _v in dict_.items():
        if isinstance(_v, dict):
            _result = findNode(_v, targetKey_)
            if _result is not None:
                return _result
    return None


if __name__ == "__main__":
    # _dict = json.loads("{\"cmd\": \"game\"}")
    # showDictStructure(_dict)
    from utils.CompanyUtil import Company_BB_Utils
    import os

    showDictStructure(
        fileUtils.dictFromJsonFile(
            os.path.join(Company_BB_Utils.getSLGProjectPath(), "svn_repos/trunk/doc/art/UI/demo/pic/局内效果图/资源建筑相关/SLG_dm_增产页界面/assets/main.json")
        )
    )
