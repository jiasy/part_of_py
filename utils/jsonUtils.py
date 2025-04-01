# !/usr/bin/env python3
# 递归将 jsonPathA_ 的内容 覆盖到 jsonPathB_ 的内容上，中保存到 jsonPathC_ 中
# 如果 jsonPathC_ 没传,则保存到 jsonPathB_ 中

import utils.fileUtils
import json
import utils.dictUtils
import utils.xmlUtils


# jsonDict 的内容合并
def mergeAToB(jsonDictA_, jsonDictB_):
    for _key in jsonDictA_:
        # 都是字典，循环键值覆盖
        if type(jsonDictA_[_key]) == dict and _key in jsonDictB_ and type(jsonDictB_[_key]) == dict:
            mergeAToB(jsonDictA_[_key], jsonDictB_[_key])
        else:
            # 不都是字典直接覆盖
            jsonDictB_[_key] = jsonDictA_[_key]
    return jsonDictB_


# jsonA_的内容会覆盖jsonB_的内容,然后保存在 jsonPathC_ 路径中
def jsonMerge(jsonPathA_, jsonPathB_, jsonPathC_=None):
    _jsonDictA = utils.fileUtils.dictFromJsonFile(jsonPathA_)
    _jsonDictB = utils.fileUtils.dictFromJsonFile(jsonPathB_)
    _jsonDictB = mergeAToB(_jsonDictA, _jsonDictB)

    # 获取写入的路径
    _targetPath = None
    if jsonPathC_:
        _targetPath = jsonPathC_
    else:
        _targetPath = jsonPathB_

    # 实际写入过程
    utils.fileUtils.writeFileWithStr(
        _targetPath,
        str(
            json.dumps(
                _jsonDictB,
                indent=4,
                sort_keys=False,
                ensure_ascii=False
            )
        )
    )


# 获取 xml 的列表，xml 转化的 dict 列表只有一个元素时不是列表，需要转换一下
def getFguiXmlDictList(containerDict_: dict, typeName_: str):
    if typeName_ not in containerDict_:
        return []
    if isinstance(containerDict_[typeName_], list):
        return containerDict_[typeName_]
    else:
        return [containerDict_[typeName_]]


# 在指定的节点上添加一个元素，如果这个节点不是数组的话就变成数组。
def addFguiXmlDictToList(containerDict_: dict, typeName_: str, xmlDict_: dict):
    if typeName_ not in containerDict_:
        containerDict_[typeName_] = []
    else:
        if not isinstance(containerDict_[typeName_], list):  # 不是数组的时候，要变成数组
            _tempDict = containerDict_[typeName_]
            containerDict_[typeName_] = [_tempDict]
    containerDict_[typeName_].append(xmlDict_)


# 修改json文件内容
def changeJsonContent(jsonPath_, writeDict_):
    _jsonDict = utils.fileUtils.dictFromJsonFile(jsonPath_)
    mergeAToB(writeDict_, _jsonDict)
    _jsonStr = str(json.dumps(_jsonDict, indent=4, sort_keys=False, ensure_ascii=False))
    utils.fileUtils.writeFileWithStr(jsonPath_, _jsonStr)


# 将 Json 转换成 C# 解析用的结构代码
def jsonToCSharpJsonSerializeCode(rootName_: str, jsonStr_: str):
    return utils.dictUtils.dictToCSharpJsonSerializeCode(rootName_, json.loads(jsonStr_))


def jsonToDotsBlobAssetCode(rootName_: str, jsonStr_: str):
    return utils.dictUtils.dictToDotsBlobAssetCode(rootName_, json.loads(jsonStr_))


def jsonToProtobufCode(rootName_: str, jsonStr_: str):
    return utils.dictUtils.dictToProtobufCode(rootName_, json.loads(jsonStr_))


if __name__ == "__main__":
    _jsonDict = utils.xmlUtils.xmlContentToDict('<image id="n8_123ebd" name="n8" src="d0da35" fileName="Texture/Ui_image_guang_03.png" xy="246,147" size="542,511" group="n4_123ebd4" aspect="true"/>')
    _id = _jsonDict["image"]["@id"]
    print('_id = ' + str(_id))
    _jsonDict["image"]["@id"] = "asdda"

    _xmlContent = utils.xmlUtils.dictToXmlContent(_jsonDict, True)
    print('_xmlContent = ' + str(_xmlContent))

    jsonStr = """
    {
        "Queue":[{
            "Id":1,
            "Status":1,
            "RelativeId":1
        }]
    }
    """
    # 生成的 protobuf
    _protobufCode = jsonToProtobufCode("QuickQueue", jsonStr)
    print(_protobufCode)














