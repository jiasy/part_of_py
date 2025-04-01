#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
from poco.drivers.unity3d import UnityPoco


class Poco(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(Poco, self).create()

    def destroy(self):
        super(Poco, self).destroy()


# 注意 这个脚本要在 3.8 下运行
if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)

    # 通过地址和端口初始化UnityPoco对象
    poco = UnityPoco('127.0.0.1', 5001)

    # 进行RPC调用，触发ExecJs方法
    poco.agent.rpc.call("ExecJs", ["console.log('AB - Hello World');"])
