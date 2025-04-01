from utils import folderUtils
from utils import fileUtils
from utils import pyServiceUtils
import os
import shutil
import json
import sys

unityProjectFolder = "/Users/nobody/Documents/develop/GitHub/UniversalRenderingExamples/"

packageCacheFolder = os.path.join(unityProjectFolder, "Library/PackageCache")
packagesFolder = os.path.join(unityProjectFolder, "Packages")

corePartName = "com.unity.render-pipelines.core"
universalPartName = "com.unity.render-pipelines.universal"

if __name__ == '__main__':
    _unityCSharpAnalyse = pyServiceUtils.getSvr(__file__)
    pyServiceUtils.printSvrCode(__file__)

    # 将 Library/packageCache 中的 core 和 universal 拷贝到 Packages 下，这样就可以对其进行修改
    _unityCSharpAnalyse.makePackageEdit(unityProjectFolder, [corePartName, universalPartName])

    # 将准备好的 LogUtils 移动到 Assets 下。
    _logUtilsMetaGuid = _unityCSharpAnalyse.syncLogUtils(os.path.join(unityProjectFolder, "Assets"))
    # 修改 Packages 下的所有 asmdef，确保其关联了 LogUtils 的 asmdef
    _unityCSharpAnalyse.linkLogUtilsAsmdef(packagesFolder, _logUtilsMetaGuid)

    # 指定文件夹添加日志
    _srpCorePath = os.path.join(packagesFolder, corePartName + "@10.7.0", "Runtime")
    _universalPath = os.path.join(packagesFolder, universalPartName + "@10.7.0", "Runtime")
    if os.path.exists(_srpCorePath) and os.path.exists(_universalPath):
        _unityCSharpAnalyse.addRunningStackLog(_srpCorePath, [])
        _unityCSharpAnalyse.addRunningStackLog(_universalPath, [])
