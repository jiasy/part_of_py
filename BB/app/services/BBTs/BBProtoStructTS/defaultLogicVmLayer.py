import os
import sys

from utils import fileUtils
from utils import strUtils


def replaceCode(templatePath_: str, codePath_: str, moduleName_: str, ):
    print(f"    生成 {fileUtils.justName(templatePath_)} : {codePath_}")
    _codeContent = fileUtils.readFromFile(templatePath_).replace("QuickQueue", moduleName_).replace("quickQueue", strUtils.lowerFirstChar(moduleName_)).replace("// @ts-ignore\n", "")
    fileUtils.writeFileWithStr(codePath_, _codeContent)


def replaceLogicCode(codeTemplateFolder_: str, moduleFolder_: str, moduleName_: str):
    # LOGIC ----------------------------------------------------------------------------------------------------------------------------- LOGIC
    _logicCodePath = os.path.join(moduleFolder_, moduleName_, f'{moduleName_}Logic.ts')
    _logicTemplatePath = os.path.join(codeTemplateFolder_, "Logic.ts")
    replaceCode(_logicTemplatePath, _logicCodePath, moduleName_)


def replaceLayerVMCode(codeTemplateFolder_: str, moduleFolder_: str, moduleName_: str):
    # LAYER ----------------------------------------------------------------------------------------------------------------------------- LAYER
    _layerCodePath = os.path.join(moduleFolder_, moduleName_, "Layer", f'{moduleName_}Layer.ts')
    _layerTemplatePath = os.path.join(codeTemplateFolder_, "Layer.ts")
    replaceCode(_layerTemplatePath, _layerCodePath, moduleName_)
    # VM ----------------------------------------------------------------------------------------------------------------------------- VM
    _vmCodePath = os.path.join(moduleFolder_, moduleName_, "VM", f'VM{moduleName_}.ts')
    _vmTemplatePath = os.path.join(codeTemplateFolder_, "VM.ts")
    replaceCode(_vmTemplatePath, _vmCodePath, moduleName_)
    # VMItem ----------------------------------------------------------------------------------------------------------------------------- VMItem
    _vmItemCodePath = os.path.join(moduleFolder_, moduleName_, "VM", f'VM{moduleName_}Item.ts')
    _vmItemTemplatePath = os.path.join(codeTemplateFolder_, "VMItem.ts")
    replaceCode(_vmItemTemplatePath, _vmItemCodePath, moduleName_)


def replaceStr(filePath_: str, keyValueList_: list):
    _lines = fileUtils.linesFromFile(filePath_)
    for _idx in range(len(_lines)):
        _line = _lines[_idx]
        for _idxLoop in range(len(keyValueList_)):
            if (_idxLoop + 1) % 2 == 0:
                _key = keyValueList_[_idxLoop - 1]
                _value = keyValueList_[_idxLoop]
                if _key in _line:
                    _lines[_idx] = _line.replace(_key, _value)
                    break  # 只换一次
    fileUtils.writeFileWithStr(filePath_, "".join(_lines))


def createLayerVMCode(codeTemplateFolder_: str, moduleFolder_: str, moduleName_: str, uiLayerName_: str):
    # 删
