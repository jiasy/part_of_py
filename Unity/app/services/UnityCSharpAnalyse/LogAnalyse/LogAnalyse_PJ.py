from Unity.app.services.UnityCSharpAnalyse.LogAnalyse import LogAnalyse
from utils import fileUtils
from utils import listUtils
from utils.CompanyUtil import Company_BB_Utils
import os


def doAssetBundleLogAnalyse(logAnalyse_: LogAnalyse):
    _patternList = [
        '''
        ''',
    ]
    logAnalyse_.analyseLogByPatterns(
        os.path.join(Company_BB_Utils.getRootFolderPath(), "C#Temp/C#Log"),
        os.path.join(Company_BB_Utils.getRootFolderPath(), "C#Temp/C#Log_test"),
        _patternList
    )


def removeLineUnderCode(logFilePath_: str, newLogFilePath_: str):
    _lines = fileUtils.linesFromFileWithOutEncode(logFilePath_)
    _newLines = []
    _mark = False  # 特殊行起始标记，后续的非代码要删除
    for _idx in range(len(_lines)):
        _line = _lines[_idx]
        if ("ThirdParty/json -> next_char" in _line) or \
                ("ThirdParty/json -> json.decode" in _line) or \
                ("ThirdParty/json -> parse" in _line):
            _mark = True
        else:
            if _line.startswith("lua ---->") or _line.startswith("C# >"):
                _mark = False
            if not _mark:
                _newLines.append(_line)

    fileUtils.writeFileWithStr(newLogFilePath_, listUtils.joinToStr(_newLines, ""))


if __name__ == '__main__':
    from utils import pyServiceUtils

    _svr = pyServiceUtils.getSubSvr(__file__)
    # doAssetBundleLogAnalyse(_svr)

    # # 删除非代码行
    # _svr.removeNotCodeLineInFile(
    #     os.path.join(Company_BB_Utils.getRootFolderPath(), "C#Temp/C#Log"),
    #     os.path.join(Company_BB_Utils.getRootFolderPath(), "C#Temp/C#Log_Lua")
    # )

    # 合并非代码行
    _svr.mergeNotCodeLineInFile(
        os.path.join(Company_BB_Utils.getRootFolderPath(), "C#Temp/C#Log"),
        os.path.join(Company_BB_Utils.getRootFolderPath(), "C#Temp/C#Log_Lua")
    )

    # removeLineUnderCode(
    #     os.path.join(Company_BB_Utils.getRootFolderPath(), "C#Temp/Run_WithLua"),
    #     os.path.join(Company_BB_Utils.getRootFolderPath(), "C#Temp/Run_WithLua_justCode")
    # )
