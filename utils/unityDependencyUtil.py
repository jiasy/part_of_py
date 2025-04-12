import sys
import utils.fileUtils
import utils.folderUtils
import re
import os
import cmdUtils


def generate_dot_text(nodes, edges, reverse_edges=False):
    """
    生成 DOT 格式的图形描述。
    :param nodes: 包含所有唯一文件路径的节点列表
    :param edges: 文件依赖关系字典，键为文件路径，值为依赖路径列表
    :param reverse_edges: 是否反转箭头方向，默认为 False
    :return: DOT 格式的图形描述字符串
    """
    # 文件扩展名到颜色的映射
    file_type_colors = {
        '.prefab': 'lightblue',  # .prefab 使用不同的颜色和圆角框
        '.unity': 'lightgreen',
        '.mat': 'orange',  # 修改 .mat 为橘黄色
        '.asset': 'lightcoral',
        '.controller': 'lightpink',
        '.playable': 'lightseagreen',
        '.timeline': 'lightcyan',
        '.bmp': 'lightgoldenrodyellow',
        '.png': 'lightskyblue',  # 保持 png 颜色为淡蓝色
        '.jpg': 'lightsteelblue',
        '.fbx': 'peachpuff',
        '.cubemap': 'wheat',
        '.exr': 'moccasin',
        '.mesh': 'lightgreen',  # 保持 mesh 颜色为绿色
        '.shader': 'lightcoral',  # 修改 .shader 为淡红色
        '.tga': 'lightblue'  # 修改 .tga 为淡蓝色，和 png 有差别
    }

    # 初始化 DOT 图表头部
    dot_text = "digraph DependencyGraph {\n"
    dot_text += "    graph [rankdir=LR];\n"  # 从左到右绘制图形，便于展示依赖关系
    dot_text += "    node [style=filled, fontsize=10, width=0.5, height=0.5];\n"  # 缩小文本框

    # 创建所有节点
    node_set = set()  # 使用集合来避免重复定义节点
    for node in nodes:
        # 将路径中特殊字符替换为下划线以防止 DOT 语法错误
        safe_node = node.replace("/", "_").replace(".", "_")
        if safe_node not in node_set:
            # 获取文件类型并选择相应的颜色
            file_extension = '.' + node.split('.')[-1] if '.' in node else ''
            fill_color = file_type_colors.get(file_extension, 'lightgrey')  # 默认为 lightgrey

            # 如果是 .prefab 文件，使用圆角框
            if file_extension == '.prefab':
                dot_text += f'    "{safe_node}" [label="{node}", fillcolor="{fill_color}", shape=rect, style=rounded, fontsize=10, width=0.5, height=0.5];\n'
            else:
                dot_text += f'    "{safe_node}" [label="{node}", fillcolor="{fill_color}",  shape=rect, fontsize=10, width=0.2, height=0.2];\n'

            node_set.add(safe_node)

    # 创建所有边
    for source, targets in edges.items():
        # 替换路径中的特殊字符以保证 DOT 文件合法性
        source_safe = source.replace("/", "_").replace(".", "_")
        for target in targets:
            target_safe = target.replace("/", "_").replace(".", "_")

            # 设置边的颜色：蓝色链接图像文件，红色链接到shader，绿色链接到mesh，橘黄色链接到mat，其他保持默认颜色
            if any(ext in target for ext in ['.png', '.tga', '.bmp', '.jpg']):
                edge_color = 'blue'  # 链接到图片类型使用蓝色线
            elif '.shader' in target:
                edge_color = 'red'  # 链接到shader文件使用红色线
            elif '.mesh' in target:
                edge_color = 'green'  # 链接到mesh文件使用绿色线
            elif '.mat' in target:
                edge_color = 'orange'  # 链接到mat文件使用橘黄色线
            else:
                edge_color = 'black'  # 默认链接颜色为黑色

            # 根据 reverse_edges 决定箭头方向
            if reverse_edges:
                dot_text += f'    "{target_safe}" -> "{source_safe}" [color="{edge_color}"];\n'
            else:
                dot_text += f'    "{source_safe}" -> "{target_safe}" [color="{edge_color}"];\n'

    # 结束 DOT 图表
    dot_text += "}\n"
    return dot_text


def getUniqueStrings(input_dict):
    unique_strings = set()  # 创建一个空集合以存储唯一字符串
    # 遍历字典中的每个键
    for key, values in input_dict.items():
        unique_strings.add(key)  # 将键添加到集合
        # 遍历值列表，添加其中的每个字符串到集合
        for value in values:
            unique_strings.add(value)
    unique_strings = list(set(unique_strings))
    return unique_strings  # 返回去重后的字符串集合


# 获取指定目录下的mat和prefab文件的meta数据
def getGuidPathDict(assetPath_):
    _guidPathDict = {}
    _pathGuidDict = {}
    _filePathList = []
    # 遍历目录及其子目录
    for _root, _, files in os.walk(assetPath_):
        for _filePath in files:
            if _filePath.endswith('.meta'):  # 扫描meta文件
                _realMetaPath = os.path.join(_root, _filePath)
                _realFilePath = _realMetaPath.split('.meta')[0]  # meta对应的文件
                if not os.path.isdir(_realFilePath):
                    with open(_realMetaPath, 'r', encoding='utf-8') as meta:
                        content = meta.read()
                        match = re.search(r'guid: ([a-f0-9]{32})', content)
                        if match:
                            guid = match.group(1)
                            relative_path = os.path.relpath(os.path.join(_root, _filePath.split('.meta')[0]), assetPath_)
                            _guidPathDict[guid] = relative_path.replace("\\", "/")
                            _pathGuidDict[_guidPathDict[guid]] = guid
                    _filePathList.append(_realFilePath.split(assetPath_ + "/")[1])
    return _guidPathDict, _pathGuidDict, _filePathList


def find_all_dependents(dependency_dict, keys):
    """
    从给定键的集合出发，递归获取所有被引用的文件集合。
    :param dependency_dict: dict, 每个键是引用者，值是被引用文件列表
    :param keys: list, 起始键或键的集合
    :return: set, 所有被引用的文件集合
    """
    # 使用集合记录访问过的节点
    visited = set()
    # DFS 递归函数
    def dfs(key):
        if key in visited:
            return
        visited.add(key)
        for dependent in dependency_dict.get(key, []):
            dfs(dependent)
    # 遍历所有起始键
    for key in keys:
        dfs(key)
    return visited


# 可以作为依赖起点的文件
def isDependencyStartFile(filePath_):
    _filePathLower = filePath_.lower()
    if _filePathLower.endswith('.prefab'):
        return True
    elif _filePathLower.endswith('.unity'):
        return True
    elif _filePathLower.endswith('.mat'):
        return True
    elif _filePathLower.endswith('.asset'):
        return True
    elif _filePathLower.endswith('.controller'):
        return True
    elif _filePathLower.endswith('.playable'):
        return True
    elif _filePathLower.endswith('.timeline'):
        return True
    return False


# 依赖关系的反向依赖关系获取
def dependencyDict_reverse(dependencyDict_):
    reverse_dependencyDict = {}
    for key, values in dependencyDict_.items():
        for value in values:
            if value not in reverse_dependencyDict:
                reverse_dependencyDict[value] = []
            reverse_dependencyDict[value].append(key)
    for _key in reverse_dependencyDict:
        reverse_dependencyDict[_key] = list(set(reverse_dependencyDict[_key]))
    return reverse_dependencyDict


class UnityDependency:
    def __init__(self, assetsPath_: str, dotsPath_: str):
        self.assetPath = assetsPath_
        self.dotsPath = dotsPath_
        self.guidPathDict, self.pathGuidDict, self.filePathList = getGuidPathDict(self.assetPath)
        self.prefabList = []
        self.unityList = []
        self.matList = []
        self.assetList = []
        self.controllerList = []
        self.playableList = []
        self.timelineList = []
        self.classifyFiles()
        self.allStartFileList = self.prefabList + self.unityList + self.matList + self.assetList + self.controllerList + self.playableList + self.timelineList
        self.pathDependencyDict = self.buildDependencyByFileList(self.allStartFileList)
        self.pathDependencyDict_reverse = dependencyDict_reverse(self.pathDependencyDict)  # 反向依赖关系

    def checkRelativePath(self, relativePath_):
        _targetPath = os.path.join(self.assetPath, relativePath_)
        if not os.path.exists(_targetPath):
            print(_targetPath + " - not exists.")
            sys.exit(1)

    # 获取指定文件夹中的依赖起点文件列表
    def getDependencyStartFileListInFolder(self, relativeFolderPath_):
        _pathList = []
        for _i in range(len(self.allStartFileList)):
            _relativeFilePath = self.allStartFileList[_i]
            if _relativeFilePath.startswith(relativeFolderPath_):
                _pathList.append(_relativeFilePath)
        return _pathList

    # 构建全工程依赖图
    def buildAllDot(self):
        self.createDotsPng("all", self.pathDependencyDict)

    # 构建指定相对文件夹的依赖图
    def buildFolderDot(self, folderPath_: str):
        self.checkRelativePath(folderPath_)  # 校验
        _filePathList = self.getDependencyStartFileListInFolder(folderPath_)  # 文件夹中的依赖起点
        self.buildDotByFileList(folderPath_, _filePathList, self.pathDependencyDict)

    # 反向构建被依赖
    def buildFileDot_reverse(self, relativeFilePath_: str):
        self.checkRelativePath(relativeFilePath_)  # 校验
        self.buildDotByFileList(relativeFilePath_, [relativeFilePath_], self.pathDependencyDict_reverse, True)

    # 构建指定文件的依赖图
    def buildFileDot(self, relativeFilePath_: str):
        self.checkRelativePath(relativeFilePath_)  # 校验
        self.buildDotByFileList(relativeFilePath_, [relativeFilePath_], self.pathDependencyDict)

    def buildDotByFileList(self, pathForName_, relativePathList_, targetPathDependencyDict_, isReverse_=False):
        _allDependencyFileSet = find_all_dependents(targetPathDependencyDict_, relativePathList_)  # 获取文件的依赖的依赖的集合
        _keyList = relativePathList_ + list(_allDependencyFileSet)  # 当前的所有文件
        _tempPathDependencyDict = {}  # 从全局依赖中摘取当前的依赖关系
        for _i in range(len(_keyList)):
            _key = _keyList[_i]
            if _key in targetPathDependencyDict_:  # 最终的被依赖对象如 png 是无法在依赖其他对象的
                _tempPathDependencyDict[_key] = targetPathDependencyDict_[_key]
        _dotName = pathForName_.replace("/", "_").replace(".", "_")
        self.createDotsPng(_dotName, _tempPathDependencyDict, isReverse_)
        cmdUtils.doStrAsCmd(f"dot {_dotName}.dot -T png -o {_dotName}.png", self.dotsPath)

    # 构建图
    def createDotsPng(self, dotName_: str, pathDependencyDict_: dict, isReverse_=False):
        _pathList = getUniqueStrings(pathDependencyDict_)  # 键 和 值列表 中出现的内容去重
        _dotsTxt = generate_dot_text(_pathList, pathDependencyDict_, isReverse_)  # 文件列表 和 这些文件 的 关系。
        _dotPath = os.path.join(self.dotsPath, dotName_ + ".dot")
        utils.fileUtils.writeFileWithStr(_dotPath, _dotsTxt)

    # 文件分类
    def classifyFiles(self):
        print("未知文件类型 : ")
        for _i in range(len(self.filePathList)):
            _filePath = self.filePathList[_i]
            _filePathLower = _filePath.lower()
            if isDependencyStartFile(_filePathLower):
                self.timelineList.append(_filePath)
            else:
                if not _filePathLower.endswith('.cs') \
                        and not _filePathLower.endswith('.lua') \
                        and not _filePathLower.endswith('.js') \
                        and not _filePathLower.endswith('.mm') \
                        and not _filePathLower.endswith('.txt') \
                        and not _filePathLower.endswith('.xml') \
                        and not _filePathLower.endswith('.json') \
                        and not _filePathLower.endswith('.plist') \
                        and not _filePathLower.endswith('.so') \
                        and not _filePathLower.endswith('.jar') \
                        and not _filePathLower.endswith('.jslib') \
                        and not _filePathLower.endswith('.asmdef') \
                        and not _filePathLower.endswith('.dll') \
                        and not _filePathLower.endswith('.a') \
                        and not _filePathLower.endswith('.ttf') \
                        and not _filePathLower.endswith('.otf') \
                        and not _filePathLower.endswith('.shadervariants') \
                        and not _filePathLower.endswith('.shader') \
                        and not _filePathLower.endswith('.cginc') \
                        and not _filePathLower.endswith('.anim') \
                        and not _filePathLower.endswith('.mesh') \
                        and not _filePathLower.endswith('.cubemap') \
                        and not _filePathLower.endswith('.exr') \
                        and not _filePathLower.endswith('.fbx') \
                        and not _filePathLower.endswith('.bytes') \
                        and not _filePathLower.endswith('.tga') \
                        and not _filePathLower.endswith('.bmp') \
                        and not _filePathLower.endswith('.jpg') \
                        and not _filePathLower.endswith('.png'):
                    print("    " + _filePath)

    def getDependencyGuidByPath(self, path_):
        """ 分析单个文件中的 GUID 引用 """
        _realFilePath = os.path.join(self.assetPath, path_)
        with open(_realFilePath, 'r', encoding='utf-8', errors='ignore') as f:
            _content = f.read()
        # 正则表达式匹配 Unity 文件中的 GUID
        _guidPattern = re.compile(r'guid:\s*([a-f0-9]{32})')
        # 查找文件中的所有 GUID
        _guids = _guidPattern.findall(_content)
        _guids = list(set(_guids))
        return _guids

    # 获取文件列表引用其他文件的列表的关系
    def buildDependencyByFileList(self, pathList_):
        print("引用文件不在工程内 : ")
        _pathDependencyDict = {}
        for _idx in range(len(pathList_)):
            _relativePath = pathList_[_idx]
            _dependencyPathList = self.buildDependencyByFile(_relativePath)
            _pathDependencyDict[_relativePath] = _dependencyPathList
        return _pathDependencyDict

    # 获取指定相对文件路径引用的其他相对路径
    def buildDependencyByFile(self, relativePath_):
        _guids = self.getDependencyGuidByPath(relativePath_)  # 获取这个文件依赖的guid列表
        _dependencyPathList = []
        for _iLoop in range(len(_guids)):
            _dependencyGuid = _guids[_iLoop]
            if _dependencyGuid not in self.guidPathDict:
                if not _dependencyGuid == "0000000000000000e000000000000000" and not _dependencyGuid == "0000000000000000f000000000000000":
                    print("    " + relativePath_ + " - " + _dependencyGuid)
                continue
            _dependencyPath = self.guidPathDict[_dependencyGuid]
            if not _dependencyPath.lower().endswith('.cs'):  # cs 文件走编译，不在依赖范畴
                _dependencyPathList.append(_dependencyPath)
        return _dependencyPathList


if __name__ == '__main__':
    _reverseStartFilePath = 'Resources/Shaders/xx.shader'
    _assetPath = "/Users/nobody/UnityProject/Assets"
    _dotPath = "/Users/nobody/Dots"
    unityDependency = UnityDependency(_assetPath, _dotPath)
    # 文件夹引用关系图
    # unityDependency.buildFolderDot("Resources/Shaders")
    # 文件引用关系图
    unityDependency.buildFileDot(_reverseStartFilePath)
    # 反向文件引用关系图
    # unityDependency.buildFileDot_reverse(_reverseStartFilePath)
