# !/usr/bin/env python3
import sys
import traceback

from git import Repo  # 导入repo模块
import utils.printUtils
import utils.strUtils
import functools
import utils.cmdUtils
import os


# 获取包含 给定字符串的 Tag 列表
# _repo = gitUtils.getRepo(本地工程路径)
def getRepo(localFolderPath_):
    return Repo.init(localFolderPath_)


# 显示是所有分支信息
def showRepoInfo(repo_):
    print("所有的分支 : ")
    utils.printUtils.printList(repo_.branches, "  ")
    print("所有未加入版本的文件 : ")
    utils.printUtils.printList(repo_.untracked_files, "  ")
    print("当前活动分支 : " + str(repo_.active_branch))
    print("当前活动分支 : " + str(repo_.head.reference))
    print("运程库 : " + str(repo_.remotes.origin))
    print("TAGs : ")
    utils.printUtils.printList(repo_.tags, "  ")


def getCurrentBiggestVersion(repo_):
    # 获取当前满足版本格式的Tag中最大的tag号
    _tagStrList = [str(_tagName) for _tagName in repo_.tags if utils.strUtils.isVersionStr(str(_tagName))]
    _tagStrList = sorted(_tagStrList, key=functools.cmp_to_key(utils.strUtils.versionCompare), reverse=True)
    return _tagStrList[0]


def getNextVersion(currentVersion_: str):
    _tagIntList = [int(_tarStr) for _tarStr in currentVersion_.split(".")]
    _tagIntList[-1] = _tagIntList[-1] + 1
    _nextTar = ".".join([str(_tarInt) for _tarInt in _tagIntList])
    return _nextTar


def is_stash_existing(repo_, _stashName):
    stash_list = repo_.git.stash('list')
    return _stashName in stash_list


def stash_changes(repo_, _stashName):
    try:
        repo_.git.stash('save', '--include-untracked', _stashName)
    except Exception as e:
        print(f"Failed to stash changes: {traceback.format_exc()}")
        sys.exit(1)


def pull_changes(repo_, branch_):
    try:
        repo_.git.pull('origin', branch_)
    except Exception as pullErr:
        print(f"Failed to pull changes: {traceback.format_exc()}")
        sys.exit(1)


def get_stash_ref(repo_, stashName_):
    _idx = 0
    for _stash in repo_.git.stash('list').splitlines():
        if stashName_ in _stash:
            return f"stash@{{{_idx}}}"
        _idx += 1
    print(f"Failed to get stash {stashName_}: {traceback.format_exc()}")
    sys.exit(1)


def apply_stash(repo_, stashName_):
    # 删


# 指定目录 path_ 拉取指定分支 branch_
def pullGitByInfo(path_: str, branch_: str):
    # 删


# 贮藏
def stash(path_: str, stashName_: str):
    if not os.path.exists(path_):
        print(f"ERROR: {path_} 不存在")
        sys.exit(1)
    _repo: Repo = Repo(path_)
    _repo.remotes.origin.fetch()
    if is_stash_existing(_repo, stashName_):
        print(f"ERROR: {path_} 贮藏 {stashName_} 已经存在")
        sys.exit(1)
    stash_changes(_repo, stashName_)


# 通过库信息的列表，拉取库
def pullGitByInfoList(gitInfoList_):
    for _pathAndBranch in gitInfoList_:
        _path, _branch = _pathAndBranch[0], _pathAndBranch[1]
        pullGitByInfo(_path, _branch)


# 创建一个标签
def createTag(repo_, tarName_):
    repo_.create_tag(tarName_)


# 获取库中的提交信息
def getCommitInfo(gitFolderPath_: str):
    _cmdStr = '''git log --pretty=format:'%H %an %ad' --date=format:'%Y-%m-%d' --numstat'''
    _pipelines = utils.cmdUtils.doStrAsCmdAndGetPipeline(_cmdStr, gitFolderPath_)
    return '\n'.join(_pipelines)


if __name__ == '__main__':
    from utils.CompanyUtil import Company_BB_Utils

    # getCommitInfo(os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts"))
    # sys.exit(1)

    stash(os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_unity"), "beforeUpgrade")
    sys.exit(1)

    _gitInfoList = [
        [os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_ts"), "dev"],
        [os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_unity"), "dev"],
        [os.path.join(Company_BB_Utils.getSLGProjectPath(), "project_config"), "master"],
        [os.path.join(Company_BB_Utils.getSLGProjectPath(), "asset_bundle"), "dev"],
        [os.path.join(Company_BB_Utils.getSLGProjectPath(), "proto"), "dev"],
    ]
    pullGitByInfoList(_gitInfoList)

    # _repo = Repo(os.path.join(Company_BB_Utils.getSLGProjectPath(), roject_ts"))
    # apply_stash(_repo, "pullGitByInfo")
