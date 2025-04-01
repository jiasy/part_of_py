#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
import utils


class Pic(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(Pic, self).create()

    def destroy(self):
        super(Pic, self).destroy()

# 获取子服务实例，获取的过程就是创建，然后创建属性关联其引用
# self.aBC = self.getSubClassObject("ABC")
# 获取自己对应资源路径 [self.resPath 为自己对应的路径，subFolder 为相对自己路径的子目录名称]
# self.resFolder = fileUtils.getPath(self.resPath, "subFolder")