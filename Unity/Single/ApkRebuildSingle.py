#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, shutil

CUR_DIR = os.path.abspath('../app/services/ApkRebuild')


def specialLog(msg):
    print('\033[1;33;40m%s\033[0m' % msg)


def decompileApk(apkName_):
    specialLog("反编译apk")
    _apkPath = os.path.join(CUR_DIR, apkName_)
    _dApkFolder = os.path.join(CUR_DIR, "deapk")
    if os.path.exists(_dApkFolder):
        shutil.rmtree(_dApkFolder)
    _cmd = "apktool d %s -o %s" % (_apkPath, _dApkFolder)
    os.system(_cmd)


def rebuildApk(apkName_, keyStore_, key_, password_):
    specialLog("重新编译出未签名apk")
    _cmd = "apktool b deapk -o temp.apk"
    os.system(_cmd)

    specialLog("重签名")
    _outputFolderPath = os.path.join(CUR_DIR, "outputs")
    if not os.path.exists(_outputFolderPath):
        os.makedirs(_outputFolderPath)

    _newApkPath = os.path.join(_outputFolderPath, apkName_)
    _cmd = "jarsigner " \
           "-verbose " \
           "-keystore %s " \
           "-storepass %s " \
           "-signedjar %s " \
           "-digestalg SHA1 " \
           "-sigalg MD5withRSA temp.apk %s" % (
               keyStore_, password_, key_, _newApkPath
           )
    os.system(_cmd)


def contentModification():
    print("修改")


'''
赋值当前脚本，和 apk 和 keystore 放置于同一个文件夹。 
    deapk 为解压出来的文件夹
    temp.apk 为临时文件
    
'''

if __name__ == '__main__':
    # 解包
    decompileApk("source.apk")

    # 修改内容
    contentModification()

    # 重新打吧
    rebuildApk("target.apk", "android.keystore", "android.keystore", "123456")
