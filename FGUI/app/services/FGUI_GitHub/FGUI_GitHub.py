#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
import os

from utils import folderUtils
from utils import fileUtils
from utils import printUtils


class FGUI_GitHub(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(FGUI_GitHub, self).create()

    def destroy(self):
        super(FGUI_GitHub, self).destroy()


fgui_unreal_folder = "/Users/nobody/Documents/develop/GitHub/FGUI/FairyGUI-unreal/Source/FairyGUI/"
head_folder = os.path.join(fgui_unreal_folder, "Public")

if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
    # 找到 h 和 cpp 文件
    h_cpp_path_list = folderUtils.getFileListInFolder(fgui_unreal_folder, [".h", ".cpp"])
    all_include_list = []
    # 通过 include 代码调用查找引用的 .h 文件路径
    for _i in range(len(h_cpp_path_list)):
        h_cpp_path = h_cpp_path_list[_i]
        include_list = fileUtils.getLinesWithStrList(h_cpp_path, ["#include"])
        trim_include_list = []
        for _iLoop in range(len(include_list)):
            trim_include_list.append(include_list[_iLoop].split(":")[1].strip())
        all_include_list = list(set(all_include_list + trim_include_list))
    # include .h 文件的相对
    h_list = []
    for _i in range(len(all_include_list)):
        all_include = all_include_list[_i]
        h_list.append(all_include.split("#include \"")[1].split("\"")[0])
    # .h 文件实际位置
    for _i in range(len(h_list)):
        _h_file_path = os.path.join(head_folder, h_list[_i])
        if not os.path.exists(_h_file_path):
            print(f"{_h_file_path}")
