#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import fileUtils
import re
import os


# 切割文本文件，成零散文件，用来切小说
class SplitTxt(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(SplitTxt, self).create()

    def destroy(self):
        super(SplitTxt, self).destroy()

    def execute(self):
        # 如果乱码的话
        # SAMPLE - iconv -f GB18030 -t UTF-8 [sourcePath] > [targetPath]
        return

    def splitFile(self, folderPath_: str, fileName_: str, targetFolderPath_: str, regStr_: str = None):
        if regStr_:
            self.splitFileReg(folderPath_, fileName_, targetFolderPath_, regStr_)
        else:
            self.splitFileWordStartLine(folderPath_, fileName_, targetFolderPath_)

    # 文章格式 : 章节标题 通过正则表达式识别 ----------------------------------------------------------------
    #   r'^\s*第([零一两俩二三四五六七八九十百千]*?)章 (.*)'
    #   r'^第(.*)章'
    def splitFileReg(self, folderPath_: str, fileName_: str, targetFolderPath_: str, regStr_: str):
        _filePath = os.path.join(folderPath_, fileName_)
        _lines = fileUtils.linesFromFile(_filePath)
        _chapterCount = 0  # 章节数
        _splitLines = []  # 内容缓存
        for _i in range(len(_lines)):
            _line = _lines[_i]
            # 找到标题，整合上一章
            _titleReg = re.search(regStr_, _line)
            if _titleReg:
                _nextLine = _lines[_i + 1]  # 连续两行都是章节名，那么就去掉下一行
                if re.search(regStr_, _nextLine):
                    _lines[_i + 1] = ""
                _chapterCount = _chapterCount + 1
                # 将之前的内容形成一个章节文件
                self.linesToFile(targetFolderPath_, _splitLines, _chapterCount)
                _splitLines = []  # 清空内容记录

            _splitLines.append(_line)  # 将当前行放入内容记录
        # 找到最后，最后一章的内容需要组合
        self.linesToFile(targetFolderPath_, _splitLines, _chapterCount)

    def linesToFile(self, targetFolderPath_: str, lines_: list, chapterCount_: int):
        # 有内容，就形成文件
        if len(lines_) > 0:
            _splitFileContent = "".join(lines_)  # 拼接内容
            _splitFileName = str(chapterCount_).rjust(3) + "_" + lines_[0] + ".txt"  # 第一行做文件名
            fileUtils.writeFileWithStr(targetFolderPath_ + "/" + _splitFileName, _splitFileContent)

    # 文章格式 : 章节标题从头起，内容缩进 ----------------------------------------------------------------
    def splitFileWordStartLine(self, folderPath_: str, fileName_: str, targetFolderPath_: str):
        _filePath = os.path.join(folderPath_, fileName_)
        _lines = fileUtils.linesFromFile(_filePath)
        # 章节数
        _chapterCount = 0
        # 内容缓存
        _splitLines = []
        # 用于切分的正则
        _contentRegStr = r'^\s.*'
        for _i in range(len(_lines)):
            _line = _lines[_i]
            _contentReg = re.search(_contentRegStr, _line)
            if not _contentReg:
                _chapterCount = _chapterCount + 1
                # 将之前的内容形成一个章节文件
                self.linesToFileWordStartLine(targetFolderPath_, _splitLines, _chapterCount)
                # 清空内容记录
                _splitLines = []
            # 将当前行放入内容记录
            _splitLines.append(_line)
        # 找到最后，最后一章的内容需要组合
        self.linesToFileWordStartLine(targetFolderPath_, _splitLines, _chapterCount)

    def linesToFileWordStartLine(self, targetFolderPath_: str, lines_: list, chapterCount_: int):
        # 有内容，就形成文件
        if len(lines_) > 0:
            _splitFileContent = "".join(lines_)  # 拼接内容
            _title = lines_[0]
            _title = _title.replace('\n', '')
            _splitFileName = str(chapterCount_ - 2).rjust(3, "0") + "_" + _title + ".txt"  # 第一行做文件名
            fileUtils.writeFileWithStr(targetFolderPath_ + "/" + _splitFileName, _splitFileContent)


if __name__ == '__main__':
    from utils import pyServiceUtils

    _svr = pyServiceUtils.getSvr(__file__)

    # 如果乱码的话
    # iconv -f GB18030 -t UTF-8 [sourcePath] > [targetPath]
    _txtFileName = "凡人修仙之仙界篇.txt"
    _txtFolderPath = "/Volumes/11/Education/小说/"
    _targetFolderPath = "/Volumes/11/Education/小说/" + _txtFileName + "章节"

    # 拆切
    _svr.splitFile(
        _txtFolderPath,
        _txtFileName,
        _targetFolderPath,
        # r'^\s*第([零一两俩二三四五六七八九十百千]*?)章 (.*)'
        #   r'^第(.*)章'
    )
