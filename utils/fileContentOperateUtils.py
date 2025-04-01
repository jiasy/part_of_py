import os.path
import sys

import utils.cmdUtils
from utils import folderUtils
from utils import fileUtils
import subprocess

import utils.printUtils


def replaceFolderStr(folderPath_: str, filterList_: list[str], fromStrList_: list[str], toStrList_: list[str]):
    if len(fromStrList_) != len(toStrList_):
        utils.printUtils.pError("ERROR : 长度不一致")
        sys.exit(1)
    _filePathList = folderUtils.getFileListInFolder(folderPath_, filterList_)
    for _i in range(len(_filePathList)):
        _filePath = _filePathList[_i]
        for _idxLoop in range(len(fromStrList_)):
            _fromStr = fromStrList_[_idxLoop]
            _toStr = toStrList_[_idxLoop]
            replaceContent(_filePath, _fromStr, _toStr)


# 替换掉内容
def replaceContent(filePath_: str, srcStr_: str, toStr_: str):
    if fileHasStr(filePath_, srcStr_) is False:  # 没有目标，无法替换
        return False
    else:  # 找到目标，进行替换
        if '/' in srcStr_ or '/' in toStr_:
            print('ERROR : 文本中包含了 /，替换无法执行')
            sys.exit(1)
        sed_command = f"LC_ALL=C sed -i '' 's/{srcStr_}/{toStr_}/g' {filePath_}"
        print('sed_command = ' + str(sed_command))
        subprocess.Popen(sed_command, shell=True).communicate()
        return True


# 替换掉内容 checkStr_ 不存在的时候才替换
def checkStrThenReplaceContent(filePath_: str, checkStr_: str, srcStr_: str, toStr_: str):
    if fileHasStr(filePath_, checkStr_) is False:  # 没有过指定文本，才进行替换
        if fileHasStr(filePath_, srcStr_) is False:  # 没有目标，无法替换
            return False
        else:  # 找到目标，进行替换
            _newContent = fileUtils.readFromFile(filePath_).replace(srcStr_, toStr_)
            fileUtils.writeFileWithStr(filePath_, _newContent)
            return True


def fileHasStr(filePath_: str, findStr_: str):
    if findStr_ is None or findStr_ == "":
        return False
    return fileHasStrList(filePath_, [findStr_])


def fileHasStrList(filePath_: str, strings_to_delete: list[str]):
    if len(strings_to_delete) == 0:
        print("没有要清理的内容")
        return False
    # 确保其全部都是字符串
    for _i in range(len(strings_to_delete)):
        if not isinstance(strings_to_delete[_i], str):
            strings_to_delete[_i] = str(strings_to_delete[_i])
    # 将字符串列表转换为grep命令的格式
    search_strings = "|".join(strings_to_delete)
    search_strings = search_strings.replace('/', '\/')
    grep_command = fr"grep -nE '{search_strings}' {filePath_}"
    print('grep_command = ' + str(grep_command))
    p1 = subprocess.Popen(grep_command, shell=True, stdout=subprocess.PIPE)
    # 文件内是否有所要删除的内容
    if p1.communicate()[0] == b"":
        print("没有匹配到任何一行")
        return False
    return True


def removeLinesWithStrList(file_path: str, strings_to_delete: list):
    if not fileHasStrList(file_path, strings_to_delete):
        return False
    # 将字符串列表转换为grep命令的格式
    search_strings = "|".join(strings_to_delete)
    search_strings = search_strings.replace('/', '\/')
    sed_command = fr"sed -i  .bak -E '/{search_strings}/d' {file_path}"
    print('sed_command = ' + str(sed_command))
    subprocess.Popen(sed_command, shell=True).communicate()
    print("成功清理")
    return True


# 去除内容相同的行
def removeDuplicationLine(filePath_: str):
    lines = fileUtils.linesFromFile(filePath_)
    stripLines = []
    for _i in range(len(lines)):
        stripLines.append(lines[_i].strip())
    fileUtils.writeFileWithStr(filePath_, "\n".join(list(set(stripLines))))


# 将两行以上的空白行变为一行
def removeMultipleBlankLine(filePath_: str):
    if not os.path.exists(filePath_):
        print(f"ERROR : {filePath_} 不存在")
        sys.exit(1)
    _cmdStr = f'''awk 'NF > 0 {{ print; seen=0 }} NF == 0 {{ if (!seen) print; seen=1 }}' "{filePath_}" > "/tmp/tmpfile" && mv "/tmp/tmpfile" "{filePath_}"'''
    utils.cmdUtils.doStrAsCmd(_cmdStr, os.path.split(filePath_)[0])


if __name__ == "__main__":
    # # 删除包含字符串的行
    # removeLinesWithStrList("/Users/nobody/Downloads/game_backup_2023.09.11-17.14.58.log.wf", ["    at "])

    # # 移除重复行
    # removeDuplicationLine("/Users/nobody/Downloads/asd.xml")

    # # 删除持有指定字符串的行
    # removeLinesWithStrList(
    #     "/disk/XS/C#Temp/Logs/PuertsLog",
    #     [
    #         "Framework/Lib/Ticker.ts -> Ticker.onUpdate",
    #         "Framework/Network/Net.ts -> NetConnection.checkTimeout",
    #         "Game/Manager/TimerManager.ts -> TimerManager.update",
    #         "Game/Module/Castle/GridMgr.ts -> GridMgr.GetNumberFromXY"
    #     ]
    # )

    removeMultipleBlankLine("/Users/nobody/Documents/develop/GitHub/Services/PY_Service/Proto/res/services/ProtoToClass/ProtoToCsClass/ExcelConfig/ExcelConfigEntry.cs")

    sys.exit(1)
