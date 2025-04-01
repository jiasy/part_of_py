#!/usr/bin/env python3
from base.supports.Base.Base import Base
from base.supports.Base.BaseInService import BaseInService
from utils import strUtils
from utils import resUtils
from utils import pyUtils
from utils import listUtils
from typing import List


class BaseService(Base):
    def __init__(self, sm_):
        super().__init__(sm_)
        # 在当前服务下创建的对象
        self.subSvrDict: dict = {}
        self.objectName: str = strUtils.lowerFirstChar(self.className)
        # 将自己的引用设置给sm
        self.sm.__setattr__(self.objectName, self)
        self.resPath: str = resUtils.getRestPathForFullClassPath(self.app.resPath, self.fullClassPath)
        # print("self.resPath = " + str(self.resPath))

    def create(self):
        super(BaseService, self).create()

    def destroy(self):
        # 当前服务下创建的对象，都要随着清理掉
        for _subClassName in self.subSvrDict:
            _subObject: BaseInService = self.subSvrDict[_subClassName]
            # 创建了，但是没销毁的，就销毁一次
            if _subObject._isCreated and not _subObject._isDestory:
                _subObject.destroy()

        super(BaseService, self).destroy()
        # 去除自己的引用
        self.sm.__delattr__(self.objectName)

    # 通过类名获取对象
    def getSubClassObject(self, subClassName_: str) -> BaseInService:
        if subClassName_ in self.subSvrDict:
            return self.subSvrDict[subClassName_]
        _subObject: BaseInService = self.sm.serviceProvider.getServiceSubObject(self, subClassName_)
        if _subObject:
            # 服务中创建的子对象，都必须继承自Base，便于统计管理
            if not isinstance(_subObject, BaseInService):
                self.raiseError(pyUtils.getCurrentRunningFunctionName(),
                                subClassName_ + " is not extends from BaseInService")
            # 服务中创建的子对象，不能是服务，免得复制粘贴代码导致的基类使用错误
            if isinstance(_subObject, BaseService):
                self.raiseError(pyUtils.getCurrentRunningFunctionName(), subClassName_ + " is BaseService")
            _subObject.create()
            self.subSvrDict[subClassName_] = _subObject
            return _subObject
        else:
            self.raiseError(pyUtils.getCurrentRunningFunctionName(), subClassName_ + " 创建失败.")
            return None
