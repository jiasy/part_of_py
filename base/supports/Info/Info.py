#!/usr/bin/env python3
import utils.printUtils
from base.supports.Base.Base import Base

from utils.pyUtils import AppError
import logging


class Info(Base):

    def __init__(self, sm_):
        super().__init__(sm_)
        logging.basicConfig(level=logging.INFO, filename='../../../' + self.app.appName + '.log')

    def create(self):
        super(Info, self).create()

    def destroy(self):
        super(Info, self).destroy()

    def raiseERR(self, errorStr_):
        utils.printUtils.pError(self.app.appName + " : " + errorStr_)
        raise AppError(errorStr_)

    def log(self, logStr_):
        logging.info(self.app.appName + " : " + logStr_)
