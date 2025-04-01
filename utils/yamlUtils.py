# !/usr/bin/env python3

from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor

import utils.fileUtils
import json
import io


# 定义你的构造方法
def my_construct_yaml_bool(self, node):
    val = self.construct_scalar(node)
    if val == "y":
        return val
    return SafeConstructor.bool_values[val]


if __name__ == '__main__':
    _yamlPath = "/Users/nobody/Documents/develop/GitRepository/Unity_2023_2D_UPR/Assets/Plugins/Shapes/Samples/Shapes Gallery.unity"
    _yamlContent = utils.fileUtils.readFromFile(_yamlPath)

    # 将它绑定到ruamel.yaml的SafeConstructor
    SafeConstructor.construct_yaml_bool = my_construct_yaml_bool

    _yaml = YAML()
    _yaml.preserve_quotes = True

    _yamlDictList = list(_yaml.load_all(_yamlContent))
    for _i in range(len(_yamlDictList)):
        _yamlDict = _yamlDictList[_i]
        _jsonContent = json.dumps(_yamlDict)
        print(_jsonContent)
        _yamlStringIo = io.StringIO()
        _yamlContent = _yaml.dump(_yamlDict, _yamlStringIo)
        _yamlStringIoStr = _yamlStringIo.getvalue()
        print(_yamlStringIoStr)
