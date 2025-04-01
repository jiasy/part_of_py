#!/usr/bin/env python3
from base.supports.Base.Base import Base
from utils import strUtils
from utils import resUtils


# 在Service中创建的Base对象
class BaseInService(Base):
    def __init__(self, belongToService_):
        super().__init__(belongToService_.sm)
        # 自己归属于哪个Service
        self.belongToService = belongToService_
        self.objectName: str = strUtils.lowerFirstChar(self.className)
        self.subResPath: str = resUtils.getRestPathForFullClassPath(self.app.resPath, self.fullClassPath)
        # print("self.subResPath = " + str(self.subResPath))

    def create(self):
        self.belongToService.__setattr__(self.objectName, self)  # 可以通过小写变量获取该对象
        super(BaseInService, self).create()

    def destroy(self):
        super(BaseInService, self).destroy()
        self.belongToService.__delattr__(self.objectName)
