from utils import folderUtils
from utils import fileUtils
from utils import pyServiceUtils
import os
import shutil
import json

runtimeFolder = "/Users/nobody/Documents/develop/GitHub/UnityPlugins/puerts_unity_demo/package/Runtime/"
srcFolder = os.path.join(runtimeFolder, "Src")

if __name__ == '__main__':
    _unityCSharpAnalyse = pyServiceUtils.getSvr(__file__)

    # 将准备好的 LogUtils 移动到 Src 下。
    _logUtilsMetaGuid = _unityCSharpAnalyse.syncLogUtils(srcFolder)

    # 修改 Packages 下的所有 asmdef，确保其关联了 LogUtils 的 asmdef
    _unityCSharpAnalyse.linkLogUtilsAsmdef(runtimeFolder, _logUtilsMetaGuid)

    # 指定文件夹添加日志
    _unityCSharpAnalyse.addRunningStackLog(srcFolder, [])
