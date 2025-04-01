from utils import folderUtils
from utils import fileUtils
from utils import pyServiceUtils
import os
import shutil
import json

unityProjectFolder = "/disk/XS/wp_client/"
packageFolder = os.path.join(unityProjectFolder, "Assets/AnimMapBaker/")

if __name__ == '__main__':
    _unityCSharpAnalyse = pyServiceUtils.getSvr(__file__)

    # 指定文件夹添加日志
    _unityCSharpAnalyse.addRunningStackLog(packageFolder, [])
