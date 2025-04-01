#!/usr/bin/env python3
import yaml

from base.supports.Service.BaseService import BaseService
from utils import folderUtils
from utils import pyServiceUtils
from utils import unityUtils
import os
from utils.CompanyUtil import Company_BB_Utils


# Animator
class UnityAnimatorController(BaseService):
    def __init__(self, sm_):
        super().__init__(sm_)

    def create(self):
        super(UnityAnimatorController, self).create()

    def destroy(self):
        super(UnityAnimatorController, self).destroy()

    def animatorWarnningPath(self, assetsPath_: str):
        unityProject = unityUtils.UnityProject(assetsPath_, [".controller", ".anim"])
        unityProject.analyseBySuffix(".controller")  # 解析指定类型
        controllerYamlList = unityProject.getYamlListBySuffix(".controller")  # 遍历指定类型的结果
        for _controlIdx in range(len(controllerYamlList)):
            _controllerYaml = controllerYamlList[_controlIdx]
            print(_controllerYaml.path + " - ing")
            _aniamtorStateList = _controllerYaml.getSubYamlsByType("AnimatorState")
            if not _aniamtorStateList:  # 可能没有 AnimatorState
                continue
            for _idx in range(len(_aniamtorStateList)):
                _subYaml = _aniamtorStateList[_idx]
                _stateNameInEditor = _subYaml.yamlDict["m_Name"]
                if _stateNameInEditor is None or _stateNameInEditor == "":
                    print(_aniamtorStateList[_idx].path + " : 的 AnimatorState 中，有 m_Name 为空的情况")
                if "guid" in _subYaml.yamlDict["m_Motion"]:  # 引用其他 anim
                    _animGuid = _subYaml.yamlDict["m_Motion"]["guid"]  # 获取 关联的 anim 的 guid
                    _stateFileIdInAnim = _subYaml.yamlDict["m_Motion"]["fileID"]  # 获取 startswith关联的 fileId
                    if unityProject.analyseGuid(_animGuid):  # 解析对应的文件，有文件就解，没文件，就证明不在当前给定的范围中
                        _animYaml = unityProject.getYamlDictByGuid(_animGuid)
                        _animClip = _animYaml.geSubYamlByFileId(_stateFileIdInAnim)  # 获取 fileId 对应的 animationClip
                        _animClipName = _animClip.yamlDict["m_Name"]
                        if _animClipName is None or _animClipName == "":
                            print(_animYaml.path + " ,fileId = " + _stateFileIdInAnim + " 的 m_Name 为空")
                        if not (_animClipName == _stateNameInEditor):
                            print(
                                "[+] {0} 中，指向 {1} 的 AnimatorState 名称和其 AnimationClip 的名称不一致".format(
                                    _aniamtorStateList[_idx].path, _animYaml.path
                                )
                            )


assetsPath = os.path.join(Company_BB_Utils.getDebugProjectFolderPath(), "Assets/")
if __name__ == '__main__':
    _svr = pyServiceUtils.getSvr(__file__)
    _svr.animatorWarnningPath(assetsPath)

    # _yamlDict = yamlUtils.yamlDictFromUnity(
    #     os.path.join(assetsPath,"Artwork/EffectWork/Animation/eff_hand_click.controller")
    # print('_yamlDict = ' + str(_yamlDict))
    # for _key in _yamlDict:
    #     print(_key)
    #     for _keyInside in _yamlDict[_key]:
    #         print("    " + _keyInside)
    # _nameFromController = _yamlDict["AnimatorController"]["m_Name"]
    # _nameFromState = _yamlDict["AnimatorState"]["m_Name"]
    # if _nameFromController != _nameFromState:
    #     print("True")
