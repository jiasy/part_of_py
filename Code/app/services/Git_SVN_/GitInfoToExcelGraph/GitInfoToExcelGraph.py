#!/usr/bin/env python3
# Created by nobody at 2023/12/24
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import gitUtils
from utils import fileUtils
from utils import folderUtils
from utils import cmdUtils
from utils import timeUtils
from utils import excelControlUtils
import os
import sys
import utils.printUtils
from datetime import datetime, timedelta
from xlwings.base_classes import Book
from xlwings.base_classes import Sheet


# 用户提交信息制表


# 每个文件
class GitCommitFile:
    def __init__(self):
        self.relativePath: str = None  # 文件路径
        self.addCount: int = 0  # 添加
        self.delCount: int = 0  # 删除

    def init(self, addCount_: int, delCount_: int, relativePath_: str):
        self.addCount = addCount_
        self.delCount = delCount_
        self.relativePath = relativePath_

    def getPrintInfo(self):
        return f'        {self.addCount} {self.delCount} {self.relativePath}'


# 每次提交
class GitCommitSingle:
    def __init__(self):
        self.commitId: str = None
        self.userName: str = None
        self.dateTime: datetime = None
        self.fileList: list[GitCommitFile] = []

    def init(self, commitId_: str, userName_: str, dateStr_: str):
        self.commitId = commitId_
        self.userName = userName_
        self.dateTime = datetime.strptime(dateStr_, "%Y-%m-%d")

    def addCommitFile(self, addCount_: int, delCount_: int, relativePath_: str):
        _gitCommitFile = GitCommitFile()
        _gitCommitFile.init(addCount_, delCount_, relativePath_)
        self.fileList.append(_gitCommitFile)

    # 添加增行
    def getAddCount(self):
        _addCount = 0
        for _i in range(len(self.fileList)):
            _addCount = _addCount + self.fileList[_i].addCount
        return _addCount

    # 添加减行
    def getDelCount(self):
        _delCount = 0
        for _i in range(len(self.fileList)):
            _delCount = _delCount + self.fileList[_i].delCount
        return _delCount

    def getPrintInfo(self):
        _backStr = f'    {self.userName} {self.dateTime.strftime("%Y-%m-%d")}'
        for _i in range(len(self.fileList)):
            _backStr = f'{_backStr}\n{self.fileList[_i].getPrintInfo()}'
        return _backStr


# 根节点
class GitCommitRoot:
    def __init__(self):
        self.commitList: list[GitCommitSingle] = []

    def init(self, gitInfoStr_: str):
        _lines = gitInfoStr_.split('\n')
        _isCommitSingle = True
        _currentCommitSingle: GitCommitSingle = None
        for _i in range(len(_lines)):
            _line = _lines[_i]

            if _isCommitSingle:
                _infoList = _line.split(" ")
                _currentCommitSingle = GitCommitSingle()
                _currentCommitSingle.init(_infoList[0], _infoList[1], _infoList[2])
                self.commitList.append(_currentCommitSingle)  # 记录这次提交
            else:
                if _line != "":
                    _infoList = _line.split(" ")
                    if len(_infoList[0]) != 40:  # 连续两行提交信息的情况排除
                        _infoList = _line.split("\t")
                        if _infoList[0] != "-" and _infoList[1] != "-":  # 排除 - 为增删信息的行
                            _currentCommitSingle.addCommitFile(int(_infoList[0]), int(_infoList[1]), _infoList[2])  # 记录提交中的文件变更信息

            # 单次提交信息行，下一行一定是提交的文件信息
            if _isCommitSingle:
                _isCommitSingle = False
            else:
                # 空白行分割开提交，所以，空白行的下一行一定是单次提交信息行
                if _line == "":
                    _isCommitSingle = True

    # 获取今天前指定天数的每一天的增减行数
    def getCommitSingleListByUserNameBeforeToday(self, userName_: str, dateNumBeforeToday_: int):
        _dayCount = dateNumBeforeToday_
        _matchingCommits: list[GitCommitSingle] = []
        _today = datetime.now()
        while _dayCount > 0:
            _dateByDiff = _today - timedelta(days=_dayCount)
            _matchingCommits += self.getCommitSingleListByUserNameInDate(userName_, _dateByDiff)
            _dayCount = _dayCount - 1
        return _matchingCommits

    # 获取指定天后面的每一天的增减行 2001-01-01
    def getCommitSingleListByUserNameAfterDate(self, userName_: str, dateFrom_: datetime, dateTo_: datetime = None):
        _dateByDiff = dateFrom_.replace(hour=0, minute=0, second=0, microsecond=0)
        if dateTo_ is None:
            _dateTo = datetime.now()
        else:
            _dateTo = dateTo_.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=24)
        _matchingCommits: list[GitCommitSingle] = []
        while _dateByDiff < _dateTo:
            _matchingCommits += self.getCommitSingleListByUserNameInDate(userName_, _dateByDiff)
            _dateByDiff = _dateByDiff + timedelta(hours=24)  # 第二天
        return _matchingCommits

    # 获取某一天的代码增删行数
    def getCommitSingleListByUserNameInDate(self, userName_: str, date_: datetime):
        _dateFrom = date_.replace(hour=0, minute=0, second=0, microsecond=0)
        _dateTo = _dateFrom + timedelta(hours=24)
        _matchingCommits: list[GitCommitSingle] = []
        for _commitSingle in self.commitList:
            if _commitSingle.userName == userName_ and _dateFrom <= _commitSingle.dateTime < _dateTo:
                _matchingCommits.append(_commitSingle)
        return _matchingCommits

    # 一天内的添加删除总量
    def get_add_del_inDate(self, userName_: str, date_: datetime):
        _matchingCommits: list[GitCommitSingle] = self.getCommitSingleListByUserNameInDate(userName_, date_)
        _addCount = 0
        _delCount = 0
        for _i in range(len(_matchingCommits)):
            _adCommits = _matchingCommits[_i]
            _addCount += _adCommits.getAddCount()
            _delCount += _adCommits.getDelCount()
        return _addCount, _delCount

    # 开始时间 dateFrom_ 和 结束时间 dateTo_ 用户 userName_ 的提交信息导入 Excel
    def commitInfoToExcel(self, dataSht: Sheet, chartSht_: Sheet, userName_: str, title_: str, dateFrom_: datetime, dateTo_: datetime = None, idx_: int = 0, xs_: float = 0.5):
        _dateByDiff = dateFrom_.replace(hour=0, minute=0, second=0, microsecond=0)
        if dateTo_ is None:
            _dateTo = datetime.now()
        else:
            _dateTo = dateTo_.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=24)
        dataSht.activate()
        # 获取数据
        _dateList = [f'{dateFrom_.year}-{dateFrom_.month}']
        _addCountList = [f'add']
        _delCountList = [f'del']
        while _dateByDiff < _dateTo:
            _addCount, _delCount = self.get_add_del_inDate(userName_, _dateByDiff)  # 用户添加和删除的行数信息
            _dateList.append(f'{_dateByDiff.month}-{_dateByDiff.day}')
            _addCountList.append(_addCount)
            _delCountList.append(_delCount)
            _dateByDiff = _dateByDiff + timedelta(hours=24)  # 第二天
        # 写入数据
        _dayNumber = len(_addCountList) - 1  # 数据长
        _column = excelControlUtils.numberToColumn(idx_ * 3 + 1)  # 第一列 add
        _columnA = excelControlUtils.numberToColumn(idx_ * 3 + 2)  # 第二列 add
        _columnB = excelControlUtils.numberToColumn(idx_ * 3 + 3)  # 第三列 del
        _column_range = f'{_column}1:{_column}{_dayNumber + 1}'  # 数据所需的范围
        _column_A_range = f'{_columnA}1:{_columnA}{_dayNumber + 1}'  # 数据所需的范围
        _column_B_range = f'{_columnB}1:{_columnB}{_dayNumber + 1}'
        dataSht.range(_column_range).options(transpose=True).value = _dateList  # 放置日期
        dataSht.range(_column_A_range).options(transpose=True).value = _addCountList  # 放置数据
        dataSht.range(_column_B_range).options(transpose=True).value = _delCountList
        # # 数据转图标
        _column_AB_range = f'{_columnA}2:{_columnB}{_dayNumber + 1}'
        # 增删
        excelControlUtils.drawDefaultChart(
            chartSht_, dataSht.range(_column_AB_range), idx_, title_, 1,
            int(_dayNumber * xs_), 10,  # 宽高
            4, "column_clustered"  # 表间距，表样式
        )
        # # 增，单独成列
        # excelControlUtils.drawDefaultChart(
        #     _sheet, _sheet.range(_column_A_range), 1, "add", 1,
        #     int(_dayNumber * 0.5), 10,  # 宽高
        #     4, "column_clustered"  # 表间距，表样式
        # )
        # # 删，单独成列
        # excelControlUtils.drawDefaultChart(
        #     _sheet, _sheet.range(_column_B_range), 2, "del", 1,
        #     int(_dayNumber * 0.5), 10,  # 宽高
        #     4, "column_clustered"  # 表间距，表样式
        # )


class GitInfoToExcelGraph(BaseInService):
    def __init__(self, belongToService_):
        super().__init__(belongToService_)
        self._nameSpace: str = None  # 命名空间
        self._gitCommitRoot: GitCommitRoot = None

    def create(self):
        super(GitInfoToExcelGraph, self).create()

    def destroy(self):
        super(GitInfoToExcelGraph, self).destroy()

    @property
    def nameSpace(self):
        if self._nameSpace is None:
            utils.printUtils.pError("ERROR : 先设置 nameSpace ")
            sys.exit(1)
        return self._nameSpace

    @nameSpace.setter
    def nameSpace(self, nameSpace_: str):
        if self._nameSpace is not None:
            utils.printUtils.pError("ERROR : nameSpace 已设置")
            return
        self._nameSpace = nameSpace_

    @property
    def gitCommitRoot(self):
        if self._gitCommitRoot is None:
            self._gitCommitRoot = self.initCacheGitInfo()
        return self._gitCommitRoot

    # 从指定命名空间获取Git信息的缓存
    def initCacheGitInfo(self):
        _cacheTxtPath = os.path.join(self.subResPath, self.nameSpace, "gitInfoCache.txt")
        if not os.path.exists(_cacheTxtPath):
            print(f"ERROR : {self.nameSpace} 没有缓存")
            sys.exit(1)
        _cacheTxtContent = fileUtils.readFromFile(_cacheTxtPath)
        _gitCommitRoot = GitCommitRoot()
        _gitCommitRoot.init(_cacheTxtContent)
        return _gitCommitRoot

    # 指定用户从库创建到现在的没日提交
    def commitInfoToExcelByUser(self, gitFolder_: str, userName_: str):
        _firstCommitDateOfThisMonth = getFirstCommitData(gitFolder_)  # 首次提交所在月的第一日
        _endOfToday = timeUtils.getEndOfToday()  # 今天的结束时间
        _excelFilePath = os.path.join(self.subResPath, self.nameSpace, f'{self.nameSpace}.xlsx')  # excel 位置
        fileUtils.removeExistFile(_excelFilePath)  # 删除原有
        _workBook: Book = excelControlUtils.openExclWorkBook(_excelFilePath)  # 创建新的
        _workBook.sheets.add(userName_)  # 添加用户
        _workBook.sheets.add(f'{userName_}_chart')
        _dataSheet = _workBook.sheets[userName_]  # 获取 用户 表
        _chartSheet = _workBook.sheets[f'{userName_}_chart']
        _betweenYearMonthList = timeUtils.getYearMonthTuplesBetween(_firstCommitDateOfThisMonth, _endOfToday)  # 获取两个日期之间的年月构成的二元组列表
        # 总表
        self.gitCommitRoot.commitInfoToExcel(_dataSheet, _chartSheet, userName_, f"ALL", _firstCommitDateOfThisMonth, _endOfToday, 0, 0.1)
        # 每月
        for _i in range(len(_betweenYearMonthList)):
            _yearMonth = _betweenYearMonthList[_i]  # 年月
            _monthBegin, _montEnd = timeUtils.getMonthBeginAndEnd(_yearMonth[0], _yearMonth[1])  # 当月的开始和结束时间
            self.gitCommitRoot.commitInfoToExcel(_dataSheet, _chartSheet, userName_, f"{_yearMonth[0]}-{_yearMonth[1]}", _monthBegin, _montEnd, _i + 1)  # 写入 用户 的数据，制表
        _workBook.save(_excelFilePath)  # 保存
        _workBook.close()


# 获取首次提交时间
def getFirstCommitData(gitFolder_: str):
    _line = cmdUtils.doStrAsCmdAndGetPipeline('git log --reverse --format=%ad --date=iso | head -n 1', gitFolder_)[0]
    # 第一次提交 '2023-02-15 17:53:25 +0800'
    _yearBegin = int(_line.split('-')[0])
    _monthBegin = int(_line.split('-')[1])
    return datetime(_yearBegin, _monthBegin, 1, 0, 0, 0)


# 缓存 Git 信息
def cacheGitInfo(subResPath_: str, nameSpace_: str, gitFolder_: str):
    _gitInfoStr = gitUtils.getCommitInfo(gitFolder_)
    _nameSpaceFolder = os.path.join(subResPath_, nameSpace_)
    folderUtils.makeSureDirIsExists(_nameSpaceFolder)
    _cacheTxtPath = os.path.join(_nameSpaceFolder, "gitInfoCache.txt")
    fileUtils.writeFileWithStr(_cacheTxtPath, _gitInfoStr)


# 打印提交信息
def printCommitSingleList(commitSingleList_: list[GitCommitSingle]):
    for _i in range(len(commitSingleList_)):
        _printStr = commitSingleList_[_i].getPrintInfo()
        print(_printStr)


if __name__ == '__main__':
    _subSvr_GitInfoToExcelGraph: GitInfoToExcelGraph = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr_GitInfoToExcelGraph.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)

    from utils.CompanyUtil import Company_BB_Utils

    _tsProjectFolder = os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts")

    # 指定命命名空间
    _subSvr_GitInfoToExcelGraph.nameSpace = "SLG"
    _subSvr_GitInfoToExcelGraph.commitInfoToExcelByUser(_tsProjectFolder, "nobody")

    sys.exit(1)

    # # 指定用户 30 天以内的信息
    # _commitList: list[GitCommitSingle] = _subSvr_GitInfoToExcelGraph.gitCommitRoot.getCommitSingleListByUserNameBeforeToday("nobody", 30)
    # printCommitSingleList(_commitList)

    # # 指定用户 指定日期内的提交
    # _inDate = datetime.strptime("2023-12-6", "%Y-%m-%d")
    # _commitList: list[GitCommitSingle] = _subSvr_GitInfoToExcelGraph.gitCommitRoot.getCommitSingleListByUserNameInDate("nobody", _inDate)
    # printCommitSingleList(_commitList)

    # # 指定用哈，指定天后的提交
    # _dataBegin = datetime.strptime("2023-12-5", "%Y-%m-%d")
    # _dateEnd = datetime.strptime("2023-12-6", "%Y-%m-%d")
    # _commitList: list[GitCommitSingle] = _subSvr_GitInfoToExcelGraph.gitCommitRoot.getCommitSingleListByUserNameAfterDate("nobody", _dataBegin, _dateEnd)
    # printCommitSingleList(_commitList)

    sys.exit(1)

    cacheGitInfo("SLG", _tsProjectFolder)
