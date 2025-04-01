from utils import pyServiceUtils
import os
import shutil
import sys
from utils import folderUtils
from Unity.app.services.UnityLuaAnalyse import UnityLuaAnalyse
from utils import sysUtils

import os
from utils.CompanyUtil import Company_BB_Utils

assetsPath = os.path.join(Company_BB_Utils.getDebugProjectFolderPath(), "Assets/")

# 打印 bundle 文件夹的结构
# folderUtils.showFileStructureReg(luaPath, [".*\.dll"])

if __name__ == '__main__':
    _subSvr = pyServiceUtils.getSubSvr(__file__)

    # # .dll
    # _subSvr.override(
    #     Company_BB_Utils.getProjectFolderPath(),
    #     os.path.join(Company_BB_Utils.getRootFolderPath(),"dlls/"),
    #     [".dll"]
    # )

    _subSvr.override(
        "/Users/nobody/Downloads/dll/",
        assetsPath,
        [".dll"]
    )
