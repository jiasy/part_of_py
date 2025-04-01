#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
from utils import cmdLogUtils
from utils import sysUtils
from utils import cmdUtils
from utils import folderUtils

'''
ApkTool 文档
    https://ibotpeaches.github.io/Apktool/documentation/
'''


def decompileApk(apkPath_, decompileTo_, apkToolPath_=None):
    cmdLogUtils.log("反编译 apk")
    folderUtils.makeSureDirIsExists(decompileTo_)
    if os.path.exists(decompileTo_):
        folderUtils.removeTree(decompileTo_)
    if apkToolPath_ == None:
        # 清理缓存的 framework ，确保 apktool 和 释放出的 framework 的一致性
        os.system("apktool empty-framework-dir")
        os.system("apktool d %s -o %s" % (apkPath_, decompileTo_))
    else:
        os.system(apkToolPath_ + " empty-framework-dir")
        os.system(apkToolPath_ + " d %s -o %s" % (apkPath_, decompileTo_))


'''
    respath = os.path.join(CUR_DIR, "deapk/assets/XM_Android")
    if os.path.exists(respath):
        folderUtils.removeTree((respath)

    # shutil.copytree(os.path.join(CUR_DIR, "XM_Android"), respath)
    shutil.copytree("XM_Android",respath)
'''

'''
jarsigner -verbose -keystore [签名文件路径] -signedjar [签名后的apk文件路径] [未签名的apk文件路径] [证书别名]
    -verbose 签名时输出详细信息，便于查看签名结果
    -keystore 私钥的绝对路径
    -signedjar 签名后apk文件存放绝对的路径
'''


def recompileApk(decompileTo_, keyStorePath_, keyPassword_, key_, targetApkFolder_, targetApkName_):
    cmdLogUtils.log("重编译 apk")
    if not os.path.exists(decompileTo_):
        cmdLogUtils.err("ERROR : Apk已解压目录不存在 " + decompileTo_)
        sys.exit(1)
    folderUtils.makeSureDirIsExists(targetApkFolder_)
    _tempApkName = "unsigned.apk"  # 临时 apk 名称
    _tempApkPath = os.path.join(targetApkFolder_, _tempApkName)  # 临时文件路径
    _targetApkPath = os.path.join(targetApkFolder_, targetApkName_)  # 目标APK路径
    if os.path.exists(_targetApkPath):
        os.remove(_targetApkPath)
    _cmd = "apktool b %s -o %s" % (decompileTo_, _tempApkName)
    cmdUtils.doStrAsCmd(_cmd, targetApkFolder_, True)
    if os.path.exists(_tempApkPath):
        cmdLogUtils.log("重签名")
        _cmd = "jarsigner -verbose -keystore %s -storepass %s -signedjar %s -digestalg SHA1 -sigalg MD5withRSA %s %s" % (
            keyStorePath_,
            keyPassword_,
            _targetApkPath,
            _tempApkPath,
            key_
        )
        os.system(_cmd)
        os.remove(_tempApkPath)  # 移除临时文件
    else:
        cmdLogUtils.err("ERROR : 重编译失败")
        sys.exit(1)


# # 要解包的apk，签名的keyStorePath，重新打包的路径，apktool的jar路径。
# _sourceApkPath = "/Volumes/Files/Downloads/916.apk"
# _decompileTo = "/Volumes/Files/Downloads/tools/deapk/"
# _keyStorePath = "/Volumes/Files/Downloads/tools/android.keystore"
# _keyPassword = "123456"
# _key = "android.keystore"
# _targetApkFolder = "/Volumes/Files/Downloads/tools/outputs/"
# _targetApkName = "newApk.apk"

'''
    工具 apktool_2.6.0.jar，解 yy.apk 到 deapk 文件夹
        java -jar /folderPath/apktool_2.6.0.jar -d /folderPath/yy.apk -o /folderPath/deapk/
    命令行执行
        python apkUtils 
            -sourceApkPath /Volumes/Files/Downloads/916.apk 
            -decompileTo /Volumes/Files/Downloads/deapk/ 
            -keyStorePath /Volumes/Files/Downloads/android.keystore
            -keyPassword 123456
            -key android.keystore
            -targetApkFolder /Volumes/Files/Downloads/outputs/
            -targetApkName newApk.apk
'''
if __name__ == '__main__':
    _thisFilePath = os.path.dirname(os.path.realpath(__file__))
    print("脚本路径 : " + _thisFilePath)
    _pwd = sysUtils.folderPathFixEnd(os.getcwd())
    print("执行路径 : " + _pwd)

    # # 定义必要参数
    # _opsDefineDict = {}
    # _opsDefineDict["sourceApkPath"]   = '源apk路径'
    # _opsDefineDict["decompileTo"]     = '反编译结果放置的文件夹'
    # _opsDefineDict["keyStorePath"]    = '秘钥库文件路径'
    # _opsDefineDict["keyPassword"]     = '秘钥库密码'
    # _opsDefineDict["key"]             = '秘钥'
    # _opsDefineDict["targetApkFolder"] = '生成apk路径'
    # _opsDefineDict["apkName"]         = '生成apk名称'
    # _opsDict = cmdUtils.getOps(_opsDefineDict, OptionParser())
    # # 获取参数
    # _sourceApkPath   = _opsDict["sourceApkPath"]
    # _decompileTo     = _opsDict["decompileTo"]
    # _keyStorePath    = _opsDict["keyStorePath"]
    # _keyPassword     = _opsDict["keyPassword"]
    # _key             = _opsDict["key"]
    # _targetApkFolder = _opsDict["targetApkFolder"]
    # _targetApkName   = _opsDict["targetApkName"]

    # 获取参数
    _baseFolder = "/disk/file/GIT/A/APKRebuild/"
    _sourceApkPath = _baseFolder + "yy.apk"
    _decompileTo = _baseFolder + "deapk/"
    _keyStorePath = _baseFolder + "android.keystore"
    _keyPassword = "123456"
    _key = "android.keystore"
    _targetApkFolder = _baseFolder + "outputs/"
    _targetApkName = "newApk.apk"

    # apktool 的路径
    _apkToolPath = "/disk/file/GIT/A/m3d/tools/packagetools/apktool.jar"

    # 反编译
    decompileApk(_sourceApkPath, _decompileTo, _apkToolPath)

    # apk 内的热更路径
    _hotFixFolderPath = _baseFolder + "deapk/assets/XM_Android/"
    if os.path.exists(_hotFixFolderPath):
        folderUtils.removeTree(_hotFixFolderPath)

    # Unity 重新构建AB包，然后拷贝进去
    shutil.copytree(
        "/disk/file/GIT/A/m3d/Assets/StreamingAssets/XM_Android",
        _hotFixFolderPath
    )

    # 编译回去
    recompileApk(_decompileTo, _keyStorePath, _keyPassword, _key, _targetApkFolder, _targetApkName)
