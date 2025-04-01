#!/usr/bin/env python3
from base.supports.Service.BaseService import BaseService
from utils import pyServiceUtils
import os
import nbformat


class JptContentAnalyse(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(JptContentAnalyse, self).create()

    def destroy(self):
        super(JptContentAnalyse, self).destroy()

    def filterLog(self, nbPath_):
        # 加载 notebook 文件
        with open(nbPath_, 'r', encoding='utf-8') as f:
            _nb = nbformat.read(f, as_version=4)
        nbformat.validate(_nb)
        # 遍历notebook中的所有cell，提取 text outputs
        for _cell in _nb['cells']:
            if _cell['cell_type'] == 'code':  # 确保单元格是代码单元格
                for _output in _cell.get('outputs', []):
                    if _output['output_type'] == 'stream' and _output['name'] == 'stdout':
                        print(''.join(_output['text']))  # 打印文本输出


if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    print('_svr.resPath = ' + str(_svr.resPath))
    pyServiceUtils.printSvrCode(__file__)

    _svr.filterLog("/Users/nobody/Documents/develop/GitHub/Services/PY_Service/JupyterLab/python/jenkins/env_jenkins.ipynb")
