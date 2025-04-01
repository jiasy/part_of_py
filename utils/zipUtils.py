# !/usr/bin/env python3
import os
import sys
import shutil
import utils.folderUtils
import utils.fileUtils
import utils.cmdUtils
import zipfile
from utils import folderUtils


# 将 folderPath_ 内的所有 zip 文件，解压到 targetFolderPath_ 中
def unZipFolderPath(folderPath_, targetFolderPath_, password_=None):
    _fileWithSuffixList = utils.folderUtils.getFilePathWithSuffixInFolder(folderPath_, ".zip")
    for _i in range(len(_fileWithSuffixList)):
        unZipPath(_fileWithSuffixList[_i], targetFolderPath_, password_)


def unZipPath(path_, targetFolderPath_, password_=None):
    print('path_ = ' + str(path_))
    _zipFile = zipfile.ZipFile(path_, 'r')
    for _subfile in _zipFile.namelist():  # f.namelist()返回列表，列表中的元素为压缩文件中的每个文件
        # 解决乱码的问题，进行一次名称转换
        try:
            _subfileNormalName = _subfile.encode('cp437').decode('gbk')
        except:
            _subfileNormalName = _subfile.encode('utf-8').decode('utf-8')
        if password_ == None:
            _zipFile.extract(_subfile, targetFolderPath_ + "/")  # 解压到给定的目录
        else:
            _zipFile.extract(_subfile, targetFolderPath_ + "/", pwd=password_.encode("utf-8"))  # 解压到给定的目录

        # 判断一下转换后的名称，如果不一致的话，就证明乱码了。
        if not _subfileNormalName == _subfile:  # 名称不一致，证明变换过
            _extractFilePath = os.path.join(targetFolderPath_, _subfile)
            _extractNormalFilePath = os.path.join(targetFolderPath_, _subfileNormalName)
            os.rename(_extractFilePath, _extractNormalFilePath)  # 将乱码名还原U
    os.remove(path_)  # 移除原有的压缩文件


# brew install unrar ，调用命令行对其进行解压
def unRarFolderPath(folderPath_, targetFolderPath_, password_=None):
    _fileWithSuffixList = utils.folderUtils.getFilePathWithSuffixInFolder(folderPath_, ".rar")
    for _i in range(len(_fileWithSuffixList)):
        unRarPath(_fileWithSuffixList[_i], targetFolderPath_, password_)


def unRarPath(path_, targetFolderPath_, password_=None):
    print('path_ = ' + str(path_))
    if not password_ == None:
        _cmdStr = 'unrar x \'{rarfilePath}\' {targetFolderPath} -p{password}'.format(
            rarfilePath=path_,
            targetFolderPath=targetFolderPath_,
            password=password_
        )
    else:
        _cmdStr = 'unrar x \'{rarfilePath}\' {targetFolderPath}'.format(
            rarfilePath=path_,
            targetFolderPath=targetFolderPath_
        )
    utils.cmdUtils.doStrAsCmd(_cmdStr, targetFolderPath_, True)
    os.remove(path_)  # 移除原有的压缩文件


def cp437ToGbk(dir_names):
    """anti garbled code"""
    os.chdir(dir_names)
    for temp_name in os.listdir('.'):
        try:
            new_name = temp_name.encode('cp437')  # 使用cp437对文件名进行解码还原
            new_name = new_name.decode("gbk")  # win下一般使用的是gbk编码
            os.rename(temp_name, new_name)  # 对乱码的文件名及文件夹名进行重命名
            temp_name = new_name  # 传回重新编码的文件名给原文件名
        except:
            pass  # 如果已被正确识别为utf8编码时则不需再编码
        if os.path.isdir(temp_name):
            cp437ToGbk(temp_name)  # 对子文件夹进行递归调用
            os.chdir('..')  # 记得返回上级目录


def removeFile(folderPath_, suffixList_):
    for _i in range(len(suffixList_)):
        _suffix = suffixList_[_i]
        _fileWithSuffixList = utils.folderUtils.getFilePathWithSuffixInFolder(folderPath_, _suffix)
        for _j in range(len(_fileWithSuffixList)):
            _fileWithSuffix = _fileWithSuffixList[_j]
            print('_fileWithSuffix = ' + str(_fileWithSuffix))
            os.remove(_fileWithSuffix)  # 移除原有的压缩文件


def renameSuffix(folderPath_, currentSuffix_, targetSuffix_):
    _fileWithSuffixList = utils.folderUtils.getFilePathWithSuffixInFolder(folderPath_, currentSuffix_)
    for _i in range(len(_fileWithSuffixList)):
        _fileWithSuffix = _fileWithSuffixList[_i]
        _justName = utils.fileUtils.justName(_fileWithSuffix)
        _dirPath = os.path.dirname(_fileWithSuffix)
        _newFileWithSuffix = os.path.join(_dirPath, _justName + targetSuffix_)
        print('_fileWithSuffix    = ' + str(_fileWithSuffix))
        print('_newFileWithSuffix = ' + str(_newFileWithSuffix))
        os.rename(_fileWithSuffix, _newFileWithSuffix)


def removeNouseFolder(parentFolder_):
    _fodlerPathList = utils.folderUtils.getFolderNameListJustOneDepth(parentFolder_)
    for _i in range(len(_fodlerPathList)):
        _folderName = _fodlerPathList[_i]
        if _folderName.find("专区") < 0:
            _folderPath = os.path.join(parentFolder_, _folderName)
            print('_folderPath = ' + str(_folderPath))
            folderUtils.removeTree(_folderPath)


if __name__ == "__main__":
    # unZipPath(
    #     "/Volumes/Files/Downloads/Unity-2018-By-Example-Second-Edition-master.zip",
    #     "/Volumes/Files/Downloads/Unity-2018/"
    # )
    # sys.exit(1)

    _folderPath = "/Users/nobody/Downloads/rar/"
    unRarFolderPath(
        _folderPath,
        _folderPath,
        "password"
    )
    sys.exit(1)

    # _folderPath = "/Volumes/DISK/学习/压缩文件/"
    # unZipFolderPath(_folderPath, _folderPath)
    # sys.exit(1)

    # # 指定文件夹内的 zip 解压
    # unZipFolderPath(
    #     "/Volumes/18511470448/绘画资源/绘师作品专区/",
    #     "/Volumes/DISK/ZIP/",
    #     "m888"
    # )
    # sys.exit(1)

    # 移除指定后缀
    removeFile("/Volumes/DISK/商业作品/", [".txt", ".url", ".pdf", ".db"])
    sys.exit(1)

    # # 后缀重命名
    # renameSuffix("/Volumes/18511470448/绘画资源/", ".downloading",".zip")
    # sys.exit(1)

    # # 后缀重命名
    # renameSuffix("/Volumes/18511470448/美术资源/商用素材专区/", ".zipVSGF",".zip")
    # sys.exit(1)

    # # 移除不包含 '专区' 字符串的文件夹
    # removeNouseFolder("/Volumes/18511470448/摄影参考/")
    # sys.exit(1)

    _folderPath = "/Volumes/18511470448/绘画资源/摄影参考专区/"
    _zipFolderPathList = utils.folderUtils.getFolderNameListJustOneDepth(_folderPath)
    for _i in range(len(_zipFolderPathList)):
        _zipFolderPath = os.path.join(_folderPath, _zipFolderPathList[_i])  # 持有 zip 的文件夹
        print('_zipFolderPath = ' + str(_zipFolderPath) + " ------------------------------------------")
        if _zipFolderPath.startswith(_folderPath):
            unZipFolderPath(_zipFolderPath, "/Volumes/18511470448/摄影参考/", "m888")  # 将其中的内容解压出来放置于持有 zip 的文件夹内
            # zip同名的文件夹列表
            _unzipFolderPathList = utils.folderUtils.getFolderNameListJustOneDepth(_zipFolderPath)
            # 解压后的文件夹中的内容，只有文件夹需要拷贝出来，其他的都删除掉
            for _j in range(len(_unzipFolderPathList)):
                _unzipFolderPath = os.path.join(_zipFolderPath, _unzipFolderPathList[_j])
                print('_unzipFolderPath       = ' + str(_unzipFolderPath))
                _usefulUnzipFolderPathList = utils.folderUtils.getFolderNameListJustOneDepth(_unzipFolderPath)
                for _k in range(len(_usefulUnzipFolderPathList)):
                    _usefulUnzipFolderPath = os.path.join(_unzipFolderPath, _usefulUnzipFolderPathList[_k])
                    print('_usefulUnzipFolderPath = ' + str(_usefulUnzipFolderPath))
                    _targetUnzipFolderPath = os.path.join(_zipFolderPath, os.path.basename(_usefulUnzipFolderPath))
                    print('_targetUnzipFolderPath = ' + str(_targetUnzipFolderPath))
                    utils.folderUtils.makeSureDirIsExists(_targetUnzipFolderPath)
                    shutil.move(_usefulUnzipFolderPath, _targetUnzipFolderPath)
                # os.remove(_unzipFolderPath)  # 移除原有的压缩文件
