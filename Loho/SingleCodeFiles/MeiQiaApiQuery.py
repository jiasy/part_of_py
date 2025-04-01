# !/usr/bin/env python3

import json
import requests
import re
import datetime
import time
import os
import getopt
import sys
import pyhdfs
import shutil
from utils import folderUtils


def requestApi(url_: str):
    r = requests.get(url_)

    response_dict = r.json()
    return response_dict


def getRequestApiUrl(url_: str, api_: str, paramDict_: dict):
    _url = url_.strip()
    if not _url[-1::] == "/":
        _url = _url + "/"
    _api = api_.strip()
    _paramList = []
    for _key in paramDict_:
        _paramList.append(_key + "=" + str(paramDict_[_key]))
    _finallUrl = _url + _api + "?" + "&".join(_paramList)
    return _finallUrl


def strToDatetime(str_: str, format_: str = None):
    _format = "%Y-%m-%d %H:%M:%S"
    if format_:
        _format = format_
    _timeArray = time.strptime(str_, _format)
    return datetime.datetime(*_timeArray[0:6])


def datetimeToStr(datetime_, format_: str = None):
    _format = "%Y-%m-%d %H:%M:%S"
    if format_:
        _format = format_
    return datetime_.strftime(_format)


def compareDatetime(datetime1_, datetime2_):
    return compareTimeStr(datetimeToStr(datetime1_), datetimeToStr(datetime2_))


# 比较时间
def compareTimeStr(timeStr1_, timeStr2_):
    _reg1 = re.search(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)', timeStr1_)
    _reg2 = re.search(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)', timeStr2_)
    if _reg1 and _reg2:
        return timeStr1_ > timeStr2_
    else:
        return None


# 等分两个时间点
def devideTwoDatetimeIntoList(datetime1_, datetime2_, datetimeTimedelta_):
    _datetimeList = [datetime1_, datetime1_ + datetimeTimedelta_]
    while not compareDatetime(_datetimeList[len(_datetimeList) - 1], datetime2_):
        _datetimeList.append(_datetimeList[-1] + datetimeTimedelta_)
    _datetimeList.pop(len(_datetimeList) - 1)
    return _datetimeList


# 写文件
def writeFileWithStr(filePath_, str_):
    if not os.path.exists(os.path.dirname(filePath_)):
        os.makedirs(os.path.dirname(filePath_))
    try:
        _file = open(filePath_, 'w')
        try:
            _file.write(str_)
        finally:
            _file.close()
    except Exception as e:
        print(filePath_, e)


def getClient(url_: str, userName_: str):
    if userName_:
        return pyhdfs.HdfsClient(hosts=url_, user_name=userName_)
    else:
        return pyhdfs.HdfsClient(hosts=url_)


def timestampToDatetime(ts_):
    return datetime.datetime.fromtimestamp(ts_)


def datetimeToTimestamp(datetime_):
    return datetime_.timestamp()


def requestMeiQiaList(beginDay_, beginTime_, endDay_, endTime_, paramJsonStr_, type_):
    if not (type_ == "tickets" or type_ == "conversations"):
        return []
    # 设置其实时间和结束时间
    _timeDict = dict({})
    _timeDict["beginDay"] = beginDay_
    _timeDict["beginTime"] = beginTime_
    _timeDict["endDay"] = endDay_
    _timeDict["endTime"] = endTime_
    # SAMPLE - string format 字典做参数
    _paramDict = json.loads(paramJsonStr_.format(**_timeDict))
    _apiUrl = getRequestApiUrl("https://api.meiqia.com/v1", type_, _paramDict)

    # 获取列表
    def _getList(apiUrlInside_):
        _apiResultDict = requestApi(apiUrlInside_)
        _listInside = _apiResultDict["result"]
        return _listInside

    # 重试次数
    _recount = 0
    _list = _getList(_apiUrl)
    # 结果为空，且重试没超过3次
    while (_list is None and _recount < 3):
        _list = _getList(_apiUrl)
        _recount = _recount + 1

    if _recount == 3:
        print(_apiUrl + "\n" + "重试次数超过三次依然没有得到结果")
        sys.exit(1)

    return _list


# 获取文件列表
def getFilterFilesInPath(path_):
    _allFilePaths = []
    for root, dirs, files in os.walk(path_):
        _realFilePaths = [os.path.join(root, _file) for _file in files]
        _allFilePaths = _allFilePaths + _realFilePaths
    return _allFilePaths


# 以某一天为基准
def getDayFromTargetDay(targetDateTime_, bufferDay_: int):
    _realDay = targetDateTime_ + datetime.timedelta(days=bufferDay_)
    return _realDay.strftime("%Y-%m-%d %H:%M:%S")


# 将起止时间作为参数，传递给脚本 注意时间格式中空格需要加'\'
# python3 MeiQiaApiQuery.py -s 2019-02-14\ 06 -e 2019-02-14\ 06 -t /tmp/ods/thirtyParty/meiQiaTmpFile -u hadoop-1.loho.local -n hadoop -f /ods/thirtyParty/meiQia -w conversations
# python3 MeiQiaApiQuery.py -s 2019-02-14\ 06 -e 2019-02-14\ 12 -t /tmp/ods/thirtyParty/meiQiaTmpFile -u hadoop-1.loho.local -n hadoop -f /ods/thirtyParty/meiQia -w tickets
if __name__ == "__main__":
    # 删
