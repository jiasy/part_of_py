#!/usr/bin/env python3
# Created by GD at 2024/6/10
from base.supports.Base.BaseInService import BaseInService
from utils import pyServiceUtils
from utils import printUtils
import sys


def read_xnb_header(file_path):
    with open(file_path, 'rb') as file:
        # 读取文件头
        signature = file.read(3).decode('utf-8')
        if signature != 'XNB':
            raise ValueError("Not a valid XNB file")

        version = int.from_bytes(file.read(1), 'little')
        platform = chr(file.read(1)[0])
        flags = int.from_bytes(file.read(1), 'little')
        file_size = int.from_bytes(file.read(4), 'little')

        print(f"Signature: {signature}")
        print(f"Version: {version}")
        print(f"Platform: {platform}")
        print(f"Flags: {flags}")
        print(f"File Size: {file_size}")


class XNB_Analyse(BaseInService):

    def __init__(self, belongToService_):
        super().__init__(belongToService_)

    def create(self):
        super(XNB_Analyse, self).create()

    def destroy(self):
        super(XNB_Analyse, self).destroy()


if __name__ == '__main__':
    _subSvr_XNB_Analyse: XNB_Analyse = pyServiceUtils.getSubSvr(__file__)
    print('_subSvr.subResPath = ' + str(_subSvr_XNB_Analyse.subResPath))
    pyServiceUtils.printSubSvrCode(__file__)
    # 示例调用
    read_xnb_header('/Volumes/things/SteamLibrary/steamapps/common/ScourgeBringer/ScourgeBringer.app/Contents/Resources/Content/Tilesets/tileset_0.xnb')
