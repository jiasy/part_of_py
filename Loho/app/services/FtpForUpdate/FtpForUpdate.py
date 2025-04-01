#!/usr/bin/env python3

from utils import ftpUtils
from base.supports.Service.BaseService import BaseService


class FtpForUpdate(BaseService):

    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(FtpForUpdate, self).create()
        print("正在获取FTP链接")
        # 获取要上传的ftp的host
        _ftpHost = "FTP网址"
        _ftpUserName = "账户"
        _ftpPassWord = "密码"
        _ftpSync = ftpUtils.getFTPSync(
            _ftpHost,
            _ftpUserName,
            _ftpPassWord,
            "文件夹/文件夹"
        )
        print("ftp链接获取成功，正在上传请稍后")
        ftpUtils.showSpecifyFileOnFtp(_ftpSync, "名称带有的字符串")

    def destroy(self):
        super(FtpForUpdate, self).destroy()


if __name__ == '__main__':
    from utils import pyServiceUtils

    _svr = pyServiceUtils.getSvr(__file__)
