# !/usr/bin/env python3
import os.path

from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from xml.etree.ElementTree import tostring
from xml.dom.minidom import parseString

import utils.fileUtils
import utils.listUtils
import utils.strUtils
import re


def xmlDictFromFile(xmlPath_: str):
    if os.path.exists(xmlPath_):
        _xmlContent = utils.fileUtils.readFromFile(xmlPath_)
        return xmlContentToDict(_xmlContent)
    else:
        return None


def xmlContentToDict(lines_: str):
    return bf.data(fromstring(lines_))


# 返回 格式化后的 xml
def dictToXmlContent(dict_: dict, asRoot_: bool):
    return formatXmlStr(tostring(bf.etree(dict_)[0], encoding="unicode"), asRoot_)


# asRoot_ 为 true 时，作为根节点需要添加 xml描述
def formatXmlStr(xmlStr_: str, asRoot_: bool = False):
    _prettyXmlStr = parseString(xmlStr_).toprettyxml()
    _prettyXmlStr = str(_prettyXmlStr).replace('<?xml version="1.0" ?>\n', "")  # 先删除xml工具生成的头
    if asRoot_:
        # 是根节点的话，添加新的指定编码的头
        _prettyXmlStr = '<?xml version="1.0" encoding="utf-8"?>\n' + _prettyXmlStr
    return utils.strUtils.removeBlankLines(_prettyXmlStr)


'''
r'.*<image .*?\/>'
'''

# 满足条件的行转换成dict，进行操作后从新写回去 func_ 返回 None 证明不需要写回去

'''

'''


def replaceXmlLine(filePath_: str, key_: str, toKey_: str, func_, startIdx_: int = 0):
    # 删


# 获得当前行的 xml 节点信息，并返回下一行序号
# 从 lines_ 的 idx_ 行找 key_ ，如果它是一个 key_ 对应的 xml 节点。返回 lines_ 被这个节点切分后的前后两段，和这个 xml 节点转换出的 dict。
def getCurrentLineNodeAndNextLineIdx(lines_: list[str], idx_: int, key_: str):
    if idx_ >= len(lines_):
        return None, None, None, None
    _line = lines_[idx_]
    _resultOneLine = re.match(r'.*<' + key_ + ' .*?\/>', _line)  # 一行
    if _resultOneLine:
        _firstPart, _xmlPart, _secondPart = utils.listUtils.listSplit(lines_, idx_, idx_)
        return idx_ + 1, _firstPart, _xmlPart, _secondPart
    _regStr = r'.*<' + key_ + ' .*?>'
    _resultMultiLine = re.match(_regStr, _line)  # 多行
    if _resultMultiLine:
        _startIdx = idx_
        while idx_ < len(lines_) - 1:
            idx_ = idx_ + 1
            _line = lines_[idx_]
            _resultMultiLineEnd = re.match(r'.*<\/' + key_ + '>', _line)
            if _resultMultiLineEnd:
                _firstPart, _xmlPart, _secondPart = utils.listUtils.listSplit(lines_, _startIdx, idx_)
                return idx_ + 1, _firstPart, _xmlPart, _secondPart
    return idx_ + 1, None, None, None


def get_fgui_xy_wh(dict_: dict):
    _xyStr = dict_["@xy"]
    _xySplit = str(_xyStr).split(",")
    _x = int(_xySplit[0])
    _y = int(_xySplit[1])
    _sizeStr = dict_["@size"]
    _whSplit = str(_sizeStr).split(",")
    _w = int(_whSplit[0])
    _h = int(_whSplit[1])
    return _x, _y, _w, _h


if __name__ == "__main__":
    _dict = xmlContentToDict('<image id="n8_123ebd" name="n8" src="d0da35" fileName="Texture/Ui_image_guang_03.png" xy="246,147" size="542,511" group="n4_123ebd4" aspect="true"/>')
    _id = _dict["image"]["@id"]
    print('_id = ' + str(_id))
    _dict["image"]["@id"] = "asdda"

    _xmlContent = dictToXmlContent(_dict, True)
    print('_xmlContent = ' + str(_xmlContent))
