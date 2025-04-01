#!/usr/bin/env python3
# Created by nobody at 2020/5/24
from base.supports.Base.BaseInService import BaseInService
import re
from utils import fileUtils
from utils import listUtils
from enum import Enum


# 行标记类型，
class LinesMarkType(Enum):
    NONE = 0
    PATTERN = 1  # 模式
    MERGE = 2  # 折叠


# 当前行类和方法名
def getClassAndFuncName(line_: str):
    '''
         Class`1 -> func
         <Class1>d__1 ->  <Class2>b__0
         [?] -> func
         Classs -> func
    '''
    _classAndFuncResult = re.search(r'.* ([\w<>?\[\]`]+) -> (\.?[\w<>]+) ?.*', line_)
    if _classAndFuncResult:
        return _classAndFuncResult.group(1), _classAndFuncResult.group(2)
    else:
        return None, None


# 当前行类和方法名的模式
def getClassAndFuncPattern(line_: str):
    _className, _funcName = getClassAndFuncName(line_)
    _classAndFuncPattern = None
    if _className and _funcName:
        _classAndFuncPattern = _className + " -> " + _funcName
    else:
        raise Exception("无法获取 funcName 和 funcName : " + line_)
    return _classAndFuncPattern


# 模板信息
class PatternInfo:
    def __init__(self, patternStr_: str):
        self.patternStr = None  # 模板源字符
        self.executeList = None  # 方法执行的模式列表
        self.lineCount = None  # 行数
        self.init(patternStr_)  # 通过给定字符串得到以上信息
        self.matchIngIdx = 0

    def init(self, patternStr_: str):
        self.patternStr = patternStr_.strip()  # 删除两侧回车和空格
        self.executeList = self.getPatternInfoList(self.patternStr)  # 执行顺序列表
        self.lineCount = len(self.executeList)

    def getPatternInfoList(self, samplePattern_: str):
        _samplePatternList = samplePattern_.split("\n")  # 切行
        _classAndFuncPatternList = []  # 模式列表
        for _idx in range(len(_samplePatternList)):
            _classAndFuncPatternList.append(getClassAndFuncPattern(_samplePatternList[_idx]))  # 模式 class -> func
        return _classAndFuncPatternList

    # 重置匹配的信息
    def matchPrepare(self):
        self.matchIngIdx = 0

    # 尝试匹配给定类和方法
    def matchClassAndFunc(self, classAndFunc_: str):
        # 匹配成功，向下推进。匹配失败还原计数
        if classAndFunc_ == self.executeList[self.matchIngIdx]:
            self.matchIngIdx += 1
            return True
        else:
            self.matchIngIdx = 0
            return False


# 行标记，模板或者折叠的起止行信息
class LinesMark:
    def __init__(self, startIdx_: int, endIdx_: int, type_: LinesMarkType):
        self.type = type_
        self.startIdx = startIdx_
        self.endIdx = endIdx_


# 匹配到的信息
class MatchInfo:
    def __init__(self):
        self.patternInfo: LinesMark = None  # 模板匹配信息
        self.mergeInfoList: list(LinesMark) = []  # 折叠匹配信息

    # 设置模板信息
    def setPatternInfo(self, patternLinesMark_: LinesMark):
        self.patternInfo = patternLinesMark_

    # 添加一次匹配的信息
    def addMergeInfo(self, mergeLinesMark_: LinesMark):
        self.mergeInfoList.append(mergeLinesMark_)


# 生成日志的二次加工，相同调用栈的内容折叠，单行递归的折叠。
class LogAnalyse(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self.logPath = None  # 目标日志路径
        self.logAnalysePath = None  # 分析后的新日志
        self.patternInfoList = None  # 模板信息列表
        self.patternStartLinesDict = None  # 模板开始位置集合
        self.patternEndLinesDict = None  # 模板结束位置集合
        self.lines = None  # 日志的每一行
        self.classAndFuncList = None  # 日志每一行构成的 "类 -> 方法" 结构
        self.lineLength = None  # 日志行数
        self.currentIdx = 0  # 当前解析的日志所在行序号

    def create(self):
        super(LogAnalyse, self).create()

    def destroy(self):
        super(LogAnalyse, self).destroy()

    # 不是指定前缀的，就是折行的。。。
    def combineLineWithOutPrefix(self, lines_: str, prefix_: str):
        _lastLineIdxWithPrefix = 0
        _newLine = []
        for _i in range(len(lines_)):
            if not lines_[_i].startswith(prefix_):
                # 去掉最后一个回车后链接
                lines_[_lastLineIdxWithPrefix] = lines_[_lastLineIdxWithPrefix][0:-1] + lines_[_i]
            else:
                # 这里记录的是上一条
                _newLine.append(lines_[_lastLineIdxWithPrefix])
                # 记录最后一个前缀存在的行号
                _lastLineIdxWithPrefix = _i
        # 记录最后一条。
        _newLine.append(lines_[-1])
        return _newLine

    # 根据给定的模板来分析日志
    def analyseLogByPatterns(self, logPath_: str, logAnalysePath_: str, patternStrList_: list):
        self.logPath = logPath_
        self.logAnalysePath = logAnalysePath_
        # 记录所有模式信息
        self.patternInfoList = []
        for _i in range(len(patternStrList_)):
            self.patternInfoList.append(PatternInfo(patternStrList_[_i]))
        # 得到每一行
        self.lines = fileUtils.linesFromFileWithOutEncode(self.logPath)
        self.lines = self.combineLineWithOutPrefix(self.lines, "C# > ")
        self.lineLength = len(self.lines)
        # 得到每一行对应的类方法名
        self.classAndFuncList = []
        for _i in range(self.lineLength):
            self.classAndFuncList.append(getClassAndFuncPattern(self.lines[_i]))
        # 当前日志偏移行号
        self.currentIdx = 0
        # 模式匹配的起止行附加的信息
        self.patternStartLinesDict = {}
        self.patternEndLinesDict = {}
        # 开始解析
        self.analyseLog()
        # 开始写日志
        self.writeLog()

    # 根据信息写日志
    def writeLog(self):
        print("添加模板起止内容，屏蔽折叠行")
        _newLines = []
        for _i in range(len(self.lines)):
            if _i in self.patternStartLinesDict:
                _newLines.append("         " + self.patternStartLinesDict[_i])
            elif _i in self.patternEndLinesDict:
                _newLines.append("         " + self.patternEndLinesDict[_i])
            _line = self.lines[_i]
            if not (_line[0] == "x"):
                _newLines.append(str(_i + 1).rjust(8) + ' ' + _line)
        print("整理后的日志写入")
        fileUtils.writeFileWithStr(
            self.logAnalysePath,
            listUtils.joinToStr(_newLines, "")
        )
        print("整理日志完毕")

    # 分析日志
    def analyseLog(self):
        # 获取需要标记的匹配信息
        _matchInfoList = self.getMatchInfoList()
        print("重写行内容")
        # 根据信息重写行
        for _i in range(len(_matchInfoList)):
            self.resetLinesByMatchInfo(_matchInfoList[_i])

    # 根据匹配信息进行编辑
    def resetLinesByMatchInfo(self, matchInfo_: MatchInfo):
        # 根据模板匹配行编辑
        self.resetLineByLinesMark(matchInfo_.patternInfo)
        _length = len(matchInfo_.mergeInfoList)
        # 记录起始
        self.patternStartLinesDict[matchInfo_.patternInfo.startIdx] = "┏".ljust(40, "━") + "\n"
        # 记录结束
        if _length == 0:
            self.patternEndLinesDict[matchInfo_.patternInfo.endIdx] = "┗".ljust(40, "━") + "\n"
        else:
            self.patternEndLinesDict[matchInfo_.patternInfo.endIdx] = ("┗<" + str(_length) + ">").ljust(40, "━") + "\n"
        # 根据折叠匹配行编辑
        for _idxInside in range(_length):
            self.resetLineByLinesMark(matchInfo_.mergeInfoList[_idxInside])

    # 根据行标记信息行编辑
    def resetLineByLinesMark(self, linesMark_: LinesMark):
        for _idx in range(linesMark_.startIdx, linesMark_.endIdx):
            self.resetLine(_idx, linesMark_.type)

    # 重置行内容
    def resetLine(self, lineIdx_: int, type_: LinesMarkType):
        _line = self.lines[lineIdx_]
        if type_ == LinesMarkType.PATTERN:
            _line = "┃" + _line[1:]
        elif type_ == LinesMarkType.MERGE:
            _line = "x" + _line[1:]
        self.lines[lineIdx_] = _line

    # 解析行，得到标记信息
    def getMatchInfoList(self):
        _matchInfoList = []
        while (self.currentIdx < self.lineLength):
            print(str(self.currentIdx) + "/" + str(self.lineLength) + " ...进行中...")
            _matchPatternInfo, _idxAfterMatch = self.matchPatternList(self.currentIdx)
            if _matchPatternInfo:
                # 第一次匹配 模式
                _startIdx = self.currentIdx
                _endIdx = _idxAfterMatch
                # 创建一个匹配信息对象
                _matchInfo = MatchInfo()
                # 记录匹配对象
                _matchInfoList.append(_matchInfo)
                # 设置匹配的模式信息
                _matchInfo.setPatternInfo(
                    LinesMark(_startIdx, _endIdx, LinesMarkType.PATTERN)
                )
                # 后续折叠行
                _mergeStartIdx = _idxAfterMatch
                # 记录成后续迭代的序号
                _tempIdx = _idxAfterMatch
                _isMegred = False
                # 判断是需要折叠，按照刚才匹配的模式，尝试继续匹配
                _match, _idxAfterMatch = self.matchPattern(_mergeStartIdx, _matchPatternInfo)
                while _match:
                    _isMegred = True
                    # 上一个成功匹配，才记录结果
                    _idxAfterMatch = _tempIdx
                    # 添加后续需要折叠的信息
                    _matchInfo.addMergeInfo(
                        LinesMark(_mergeStartIdx, _idxAfterMatch, LinesMarkType.MERGE)
                    )
                    # 在上一个结果的基础上，偏移一个
                    _mergeStartIdx = _idxAfterMatch
                    # 做下一次匹配尝试
                    _match, _tempIdx = self.matchPattern(_mergeStartIdx, _matchPatternInfo)
                if not _isMegred:
                    self.currentIdx = _endIdx
                else:
                    # 语句标示向下迁移。
                    self.currentIdx = _idxAfterMatch
            else:
                self.currentIdx = self.currentIdx + 1
        return _matchInfoList

    # 从给定行号开始进行所有模式匹配
    def matchPatternList(self, curIdx_: int):
        _idxAfterMatch = -1
        _matchPatternInfo = None
        for _idx in range(len(self.patternInfoList)):
            # 用给定的行号作为起点去匹配各个模式
            _match, _idxAfterMatch = self.matchPattern(curIdx_, self.patternInfoList[_idx])
            if _match:
                _matchPatternInfo = self.patternInfoList[_idx]
                break
        return _matchPatternInfo, _idxAfterMatch

    # 从给定行号起，进行指定模式匹配
    def matchPattern(self, startIdx_: int, patternInfo_: PatternInfo):
        patternInfo_.matchPrepare()  # 准备匹配
        _length = len(self.classAndFuncList)
        for _idx in range(startIdx_, startIdx_ + patternInfo_.lineCount):  # 模板行数，进行匹配
            if _idx >= _length:
                return False, -1  # 行不够了
            if not patternInfo_.matchClassAndFunc(self.classAndFuncList[_idx]):  # 任何一行，没有匹配到
                return False, -1  # 返回未匹配
        return True, startIdx_ + patternInfo_.lineCount  # 匹配到，返回匹配后的行号偏移

    # -------------------------------------------------------------------------------------------------
    # 去掉文件中不是代码堆栈的部分
    def removeNotCodeLineInFile(self, logFilePath_: str, justCodeLogFilePath_: str):
        _lines = fileUtils.linesFromFileWithOutEncode(logFilePath_)
        _lines = self.removeNotCodeLine(_lines)
        fileUtils.writeFileWithStr(justCodeLogFilePath_, listUtils.joinToStr(_lines, ""))

    # 去掉不是代码堆栈的部分
    def removeNotCodeLine(self, lines_: list):
        _newLines = []
        for _i in range(len(lines_)):
            _line = lines_[_i]
            if _line.startswith("C#") or _line.startswith("lua"):
                _newLines.append(_line)
        return _newLines

    # 合并不是代码的部分
    def mergeNotCodeLineInFile(self, logFilePath_: str, justCodeLogFilePath_: str):
        _lines = fileUtils.linesFromFileWithOutEncode(logFilePath_)
        _lines = self.mergeNotCodeLine(_lines)
        fileUtils.writeFileWithStr(justCodeLogFilePath_, listUtils.joinToStr(_lines, ""))

    # 不是代码的行合并到上面第一个非代码行上
    def mergeNotCodeLine(self, lines_: list):
        _newLines = []
        for _i in range(len(lines_)):
            _line = lines_[_i]
            if _line.startswith("C#") or _line.startswith("lua"):
                _newLines.append(_line)
            else:
                # 最后一行
                _lastLine = _newLines[-1]
                # 掉最后面的回车，衔接当前行
                _newLines[-1] = str(_lastLine[0:-1]) + _line
        return _newLines

# if __name__ == '__main__':
#     from utils import pyServiceUtils
#
#     _svr = pyServiceUtils.getSubSvr(__file__)
