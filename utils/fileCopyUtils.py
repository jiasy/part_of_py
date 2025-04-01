#!/usr/bin/env python3
import json
import os
import shutil
import utils.sysUtils
import utils.folderUtils


# 文件夹 同结构拷贝
# # 只拷贝 jpg 和 png 到指定文件夹
# fileCopyUtils.copyFilesInFolderTo([".jpg",".png"],"原路径","目标路径","include",false) # 只拷贝后缀列表中的
# # 排除 .meta 文件拷贝到指定文件夹爱
# fileCopyUtils.copyFilesInFolderTo([".meta"],"原路径","目标路径","exclude",false)
def copyFilesInFolderTo(suffixList_: list, src_root: str, dst_root: str, type_: str = "include", log_: bool = False):
    _configObject = {}
    _configObject["from"] = ""
    _configObject["to"] = ""
    _configObject[type_] = []
    for _i in range(len(suffixList_)):
        _suffix = suffixList_[_i]
        _configObject[type_].append("*" + _suffix + "$")
    copyFilesWithConfig([_configObject], src_root, dst_root, log_)


# 根据配置结构拷贝
def copyFilesWithConfig(config_, srcRoot_, dstRoot_, log_):
    for _i in range(len(config_)):
        copyFilesWithConfigSingle(config_[_i], srcRoot_, dstRoot_, log_)


# 拷贝文件夹---------------------------------------------------------------------------------------
def copyFilesInDir(src_, dst_, log_: bool = False, filters_: list[str] = None):
    # 删


# 拷贝文件
def copyFile(src_, dst_):
    shutil.copy(src_, dst_)


def copyFilesWithConfigSingle(config_, srcRoot_, dstRoot_, log_):
    _srcDir = config_["from"]
    _dstDir = config_["to"]
    _srcDir = os.path.join(srcRoot_, _srcDir)
    _dstDir = os.path.join(dstRoot_, _dstDir)
    _includeRules = None
    if "include" in config_:
        _includeRules = config_["include"]
        _includeRules = convert_rules(_includeRules)

    _excludeRules = None
    if "exclude" in config_:
        _excludeRules = config_["exclude"]
        _excludeRules = convert_rules(_excludeRules)

    copyFilesWithRules(
        _srcDir, _srcDir, _dstDir, log_, _includeRules, _excludeRules)


def copyFilesWithRules(srcRootDir_, src_, dst_, log_, include_=None, exclude_=None):
    if os.path.isfile(src_):
        _copySrc = src_
        _copyDst = utils.sysUtils.folderPathFixEnd(dst_)
        utils.folderUtils.makeSureDirIsExists(_copyDst)
        shutil.copy(_copySrc, _copyDst)
        return

    if (include_ is None) and (exclude_ is None):
        utils.folderUtils.makeSureDirIsExists(dst_)
        copyFilesInDir(src_, dst_, log_)
    elif (include_ is not None):
        # have include
        for _name in os.listdir(src_):
            _absPath = os.path.join(src_, _name)
            _relPath = os.path.relpath(_absPath, srcRootDir_)
            if os.path.isdir(_absPath):
                _subDst = os.path.join(dst_, _name)
                copyFilesWithRules(
                    srcRootDir_,
                    _absPath,
                    _subDst,
                    log_,
                    include_=include_
                )
            elif os.path.isfile(_absPath):
                if _in_rules(_relPath, include_):
                    _copyDst = utils.sysUtils.folderPathFixEnd(dst_)
                    utils.folderUtils.makeSureDirIsExists(_copyDst)
                    shutil.copy(_absPath, _copyDst)
    elif (exclude_ is not None):
        # have exclude
        for _name in os.listdir(src_):
            _absPath = os.path.join(src_, _name)
            _relPath = os.path.relpath(_absPath, srcRootDir_)
            if os.path.isdir(_absPath):
                _subDst = os.path.join(dst_, _name)
                copyFilesWithRules(srcRootDir_, _absPath, _subDst, log_, exclude_=exclude_)
            elif os.path.isfile(_absPath):
                if not _in_rules(_relPath, exclude_):
                    _copyDst = utils.sysUtils.folderPathFixEnd(dst_)
                    utils.folderUtils.makeSureDirIsExists(_copyDst)
                    shutil.copy(_absPath, _copyDst)


def _in_rules(relPath_, rules_):
    import re
    _ret = False
    _pathStr = relPath_.replace("\\", "/")
    for _rule in rules_:
        if re.match(_rule, _pathStr):
            _ret = True
    return _ret


def convert_rules(rules):
    _retRules = []
    for _rule in rules:
        _ret = _rule.replace('.', '\\.')
        _ret = _ret.replace('*', '.*')
        _ret = "%s" % _ret
        _retRules.append(_ret)
    return _retRules


# 复制文件去文件夹
def copyFilesToFolder(fileList_: list, folderPath_: str):
    _folderPath = utils.sysUtils.folderPathFixEnd(folderPath_)
    utils.folderUtils.makeSureDirIsExists(folderPath_)
    for _i in range(len(fileList_)):
        _filePath = fileList_[_i]
        _baseName = os.path.basename(_filePath)
        _targetPath = _folderPath + _baseName
        shutil.copy(_filePath, _targetPath)


if __name__ == "__main__":
    # 拷贝图片
    copyFilesInFolderTo(
        [".cs"],
        "/Users/nobody/Documents/develop/GitRepository/Unity_2023_2D_UPR/Assets/Plugins/FGUI/",
        "/Users/nobody/Documents/develop/GitHub/Services/CS_Service/FGUI/"
    )



