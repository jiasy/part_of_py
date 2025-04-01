# !/usr/bin/env python3
import random
import re
import json
import string
from typing import List

import utils.folderUtils

# 移除掉一些麻烦的字符串
chars = {
    '\xc2\x82': ',',  # High code comma
    '\xc2\x84': ',,',  # High code double comma
    '\xc2\x85': '...',  # Tripple dot
    '\xc2\x88': '^',  # High carat
    '\xc2\x91': '\x27',  # Forward single quote
    '\xc2\x92': '\x27',  # Reverse single quote
    '\xc2\x93': '\x22',  # Forward double quote
    '\xc2\x94': '\x22',  # Reverse double quote
    '\xc2\x95': ' ',
    '\xc2\x96': '-',  # High hyphen
    '\xc2\x97': '--',  # Double hyphen
    '\xc2\x99': ' ',
    '\xc2\xa0': ' ',
    '\xc2\xa6': '|',  # Split vertical bar
    '\xc2\xab': '<<',  # Double less than
    '\xc2\xbb': '>>',  # Double greater than
    '\xc2\xbc': '1/4',  # one quarter
    '\xc2\xbd': '1/2',  # one half
    '\xc2\xbe': '3/4',  # three quarters
    '\xca\xbf': '\x27',  # c-single quote
    '\xcc\xa8': '',  # modifier - under curve
    '\xcc\xb1': ''  # modifier - under line
}


def removeBlankLines(content_: str):
    content_ = content_.replace("&#xD;", "").replace("&#xA;", "")
    _contentLines = str(content_).split('\n')
    if len(_contentLines) > 0:
        _newContent = ""
        for _i in range(len(_contentLines)):
            _line = _contentLines[_i]
            if not _line.strip() == "":
                _newContent = _newContent + _line
                if _i != (len(_contentLines) - 1):
                    _newContent = _newContent + '\n'
        return _newContent
    else:
        return content_


# 匹配到的为 key，这里得到的就是返回 value
def replace_chars(match):
    return chars[match.group(0)]


# 替换字符串
# str_ 中的 sourceStr_ 替换成 targetStr_
def replaceStr(str_: str, sourceStr_: str, targetStr_: str):
    str_ = str_.replace(sourceStr_, targetStr_)
    return str_


# 把 chars 中的字符串做 key，替换成对应 value
def removeAnnoyingChars(targetStr_):
    return re.sub(r'(' + '|'.join(chars.keys()) + ')', replace_chars, targetStr_)


# 首字母小写
def lowerFirstChar(str_: str):
    return str_[0].lower() + str_[1:]


def upperFirstChar(str_: str):
    return str_[0].upper() + str_[1:]


def convertToInt(str_):
    _subInt = pow(10, len(str_))
    str_ = "1" + str_
    if (type(eval(str_)) == int):
        _current = int(str_)
        _target = _current - _subInt
        return _target
    else:
        raise Exception(str_ + " is not a int.")


# 判断字符串是否是数字
def is_number(str_):
    try:
        float(str_)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(str_)
        return True
    except (TypeError, ValueError):
        pass

    return False


# # match 就是识别字符串是否以表达式开头
# # 以 . 开头的字符串
# re.match(r'\..*')
# # 以 双下岗线开头的字符串
# re.match(r'__.*')
# # 以 任意字符串 开头，.pyc结尾的字符串
# re.match(r'.*\.pyc')
# # 完整文件名
# re.match(r'metastore_db')
#
# _reStrList = [
#     '\..*',
#     '__.*',
#     '.*\.pyc',
#     'metastore_db'
# ]
# strUtils.isStrInFilterRegList(_reStrList,".git")

def isStrInFilterRegList(filterList_, str_):
    for _rStr in filterList_:
        if re.match(_rStr, str_):
            return True
    return False


# 多个连续空格变成一个空格,去两边空格
def spacesReplaceToSpace(str_):
    return re.sub(r' +', ' ', str_).lstrip().rstrip()


# 多行矩阵字符串 转换成 矩阵。每一个行为第二维度，每一行内的通过分割符的构成第一维
def strToMatrix(str_: str, splitStr_: str = ","):
    _lines = str_.split("\n")
    _matrix = []
    for _line in _lines:
        if not _line == "":
            _matrix.append(_line.split(splitStr_))
    return _matrix


# str_ 中 出现多少次 char_
def charCount(str_: str, char_: str):
    return list(str_).count(char_)


# str_ 中 出现多少次 strInsider_。最后一次结尾在哪里
def strCount(str_: str, strInside_: str):
    _count: int = -1
    _findIdx: int = 0
    while _findIdx != -1:
        _findIdx = str_.find(strInside_, _findIdx + len(strInside_))
        _count = _count + 1
    return _count, _findIdx + len(strInside_)


# 版本号比较
# _compareInt = strUtils.versionCompare("1.1.2", "1.1.3")
# if (_compareInt == 1):  # 1大2小
#
# elif (_compareInt == -1):  # 2大1小
#
# elif (_compareInt == 0):  # 相同
#
# elif:  # 版本号出错
def versionCompare(v1: str = "1.1.1", v2: str = "1.2"):
    if not isVersionStr(v1) or not isVersionStr(v2):
        return None
    v1_list = v1.split(".")
    v2_list = v2.split(".")
    v1_len = len(v1_list)
    v2_len = len(v2_list)
    if v1_len > v2_len:
        for i in range(v1_len - v2_len):
            v2_list.append("0")
    elif v2_len > v1_len:
        for i in range(v2_len - v1_len):
            v1_list.append("0")
    else:
        pass
    for i in range(len(v1_list)):
        if int(v1_list[i]) > int(v2_list[i]):
            return 1  # v1大
        if int(v1_list[i]) < int(v2_list[i]):
            return -1  # v2大
    return 0  # 相等


# 检测当前名称是否是版本号
def isVersionStr(ver_: str):
    _verCheck = re.match("\d+(\.\d+){0,2}", ver_)
    if _verCheck is None or _verCheck.group() != ver_:
        return False
    else:
        return True


# 检查当前行，从指定位开始，是不是想要的字符串，并且，返回找到后，刨去字符串的新位置
def checkStr(line_: str, idx_: int, checkStr_: str):
    _commentLiength = len(checkStr_)
    if idx_ + _commentLiength <= len(line_):
        if line_[idx_:idx_ + _commentLiength] == checkStr_:
            return (True, idx_ + _commentLiength)
    return (False, idx_)


def replaceKeyToValueInTemplate(replaceDict_: dict, templateStr_: str):
    '''
    模板里面的键，替换成给定字典中的对应键的值
        # {{ 表示 { , {aKey} 是替换部分，所以是 {{{aKey}}}
        _str = replaceKeyToValueInTemplate({"aKey": "aValue", "bKey": "bValue"}, "{{{aKey}:{bKey}}}")
        print(_str) # 键值对儿替换 {aKey:bKey} -> {aValue:bValue}
    '''
    return templateStr_.format(**replaceDict_)


def removePrefix(name_: str, splitStr_: str = "_"):
    return splitStr_.join(name_.split(splitStr_)[1:])


def isAContainB(aStr_: str, bStr_: str):
    return bStr_ in aStr_


# 一定会分成两部分的
def splitToAB(str_: str, split_: str):
    if split_ in str_:
        _strList = str_.split(split_)
        if len(_strList) == 2:
            return _strList[0], _strList[1]
        else:
            return None, None
    else:
        return None, None


# 一定会分成三分
def splitToABC(str_: str, split_: str):
    if split_ in str_:
        _strList = str_.split(split_)
        if len(_strList) == 3:
            return _strList[0], _strList[1], _strList[2]
        else:
            return None, None, None
    else:
        return None, None, None


# 数组中的任何一个都是切分符来切字符串
def splitByList(targetStr_: str, splitStrList_: list):
    # 按照长度由长到短排序
    splitStrList_ = sorted(splitStrList_, key=lambda _x: len(_x), reverse=True)
    # 将传进来的列表放入统一的数组中
    _resultSplit = [targetStr_]
    # 使用for循环每次处理一种分割符
    for _sep in splitStrList_:
        # 用于暂时存储分割中间列表变量
        _stringTemp = []
        # 使用map函数迭代 _resultSplit 字符串数组
        list(
            map(
                lambda sub_string_: _stringTemp.extend(sub_string_.split(_sep)),
                _resultSplit
            )
        )
        # 经过上面的指令，中间变量 _stringTemp 就被分割后的内容填充了，将分割后的内容赋值给 _resultSplit，并作为函数返回值即可
        _resultSplit = _stringTemp

    return _resultSplit


def folderToTxt(folderPath_: str, filterList_: List[str], txtPath_: str):
    _fileList = utils.folderUtils.getFileListInFolder(folderPath_, filterList_)
    _finalFileContent = []
    for _i in range(len(_fileList)):
        _filePath = _fileList[_i]
        _lines = utils.fileUtils.linesFromFile(_filePath)
        _finalFileContent += f"以下为 {[_filePath.split(folderPath_)[1]]} 内容 : \n"
        _finalFileContent += _lines
        _finalFileContent += ["\n"]
    utils.fileUtils.writeFileWithStr(txtPath_, "".join(_finalFileContent))


def isValidCodeName(name: str) -> bool:
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    if re.match(pattern, name):
        return True
    else:
        return False


def isNumUnderscore(str_: str) -> bool:
    pattern = r'^[a-zA-Z0-9_]*$'
    if re.match(pattern, str_):
        return True
    else:
        return False


def getRandomId():
    magic_number = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(1))
    s1 = '0000' + str(hex(random.randint(0, 1679615)))[2:]
    s2 = '000' + str(hex(random.randint(0, 46655)))[2:]
    count = 0
    for i in range(4):
        c = random.randint(0, 25)
        count += pow(26, i) * (c + 10)
    count += random.randint(0, 999999) + random.randint(0, 222639)
    return magic_number + s1[-4:] + s2[-3:] + str(hex(count))[2:]


'''
SAMPLE
    path_[0:path_.rindex('/')]
    右侧第一个 '/' 所在序号，从头切分路径直至这个序号。
'''
if __name__ == "__main__":
    # # {{ 标示 { , {aKey} 是替换部分，所以是 {{{aKey}}}
    # _str = replaceKeyToValueInTemplate({"aKey": "aValue", "bKey": "bValue"}, "{{{aKey}:{bKey}}}")
    # print("TActivityDailyDealSetHeroTmpIdReq".upper())

    folderToTxt(
        "/Users/nobody/Downloads/策略思维/",
        [".js", ".csv", ".bat", ".json"],
        "/Users/nobody/Downloads/策略思维.txt"
    )
