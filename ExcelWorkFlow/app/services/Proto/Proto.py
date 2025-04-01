#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from ExcelWorkFlow.app.services.Proto.PbCreator import PbCreator
from utils import fileCopyUtils
from utils import pyServiceUtils


class Proto(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)
        self.pbCreator: PbCreator = None

    def create(self):
        super(Proto, self).create()
        self.pbCreator = self.getSubClassObject("PbCreator")

    def destroy(self):
        super(Proto, self).destroy()

    def createPbFile(self):
        fileCopyUtils.copyFilesInFolderTo(
            [".proto"],
            "/disk/SY/protocol_farm/server/",
            "/disk/SY/openresty/proto/",
            "include",
            True
        )

        # 通过命令行驱动pb文件生成
        self.pbCreator.createPbFile(
            "/disk/SY/openresty/proto/",
            "/disk/SY/openresty/app/lua/protobuf/pb/"
        )


if __name__ == '__main__':
    _svr: Proto = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)
    _svr.createPbFile()
