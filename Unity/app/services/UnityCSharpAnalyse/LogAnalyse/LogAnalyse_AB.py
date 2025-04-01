from Unity.app.services.UnityCSharpAnalyse.LogAnalyse import LogAnalyse


def doAssetBundleLogAnalyse(logAnalyse_: LogAnalyse):
    _patternList = [
        '''
C# >   |   |   |   |   AssetTarget -> Analyze
C# >   |   |   |   |   |   AssetTarget -> LoadMetaHashIfNecessary
C# >   |   |   |   |   |   AssetBundleUtils -> GetCacheInfo 
C# >   |   |   |   |   |   AssetTarget -> GetHash
C# >   |   |   |   |   |   |   AssetBundleUtils -> GetFileHash 
C# >   |   |   |   |   |   |   |   HashUtil -> Get
C# >   |   |   |   |   |   |   |   |   HashUtil -> ToHexString
C# >   |   |   |   |   |   AssetTarget -> isFilterAtlas
C# >   |   |   |   |   |   AssetTarget -> FilterModel
C# >   |   |   |   |   |   |   AssetPostProcessor -> isNeedReImport 
C# >   |   |   |   |   |   |   |   AssetPostProcessor -> readCacheInfo
C# >   |   |   |   |   |   AssetTarget -> FilterAnimator
C# >   |   |   |   |   |   AssetTarget -> isFilerBuildInRes
C# >   |   |   |   |   |   AssetBundleUtils -> Load
C# >   |   |   |   |   |   |   AssetBundleUtils -> Load
C# >   |   |   |   |   |   AssetTarget -> AddDependChild
C# >   |   |   |   |   |   AssetTarget -> Analyze
        ''',
        # 分析 spritealtas 调用栈
        '''
C# >   |   |   AssetBundleUtils -> Load
C# >   |   |   |   AssetBundleUtils -> Load
C# >   |   |   |   |   AssetTarget -> .ctor 
C# >   |   |   |   |   |   AssetBundleUtils -> ConvertToABName 
C# >   |   |   |   |   |   HashUtil -> Get 
C# >   |   |   |   |   |   |   HashUtil -> Get
C# >   |   |   |   |   |   |   |   HashUtil -> ToHexString
C# >   |   |   |   |   |   AssetTarget -> analyAtlas
        ''',
        # 分析 prefab 调用栈
        '''
C# >   |   |   AssetBundleUtils -> Load
C# >   |   |   |   AssetBundleUtils -> Load
C# >   |   |   |   |   [?] -> LoadMainAssetAtPath
C# >   |   |   |   |   |   Empty4Raycast -> .ctor
C# >   |   |   |   |   AssetTarget -> .ctor 
C# >   |   |   |   |   |   AssetBundleUtils -> ConvertToABName 
C# >   |   |   |   |   |   HashUtil -> Get 
C# >   |   |   |   |   |   |   HashUtil -> Get
C# >   |   |   |   |   |   |   |   HashUtil -> ToHexString
        ''',
        # 分析 lua 调用栈
        '''
C# >   |   |   AssetBundleUtils -> Load
C# >   |   |   |   AssetBundleUtils -> Load
C# >   |   |   |   |   AssetTarget -> .ctor 
C# >   |   |   |   |   |   AssetBundleUtils -> ConvertToABName 
C# >   |   |   |   |   |   HashUtil -> Get 
C# >   |   |   |   |   |   |   HashUtil -> Get
C# >   |   |   |   |   |   |   |   HashUtil -> ToHexString
        ''',
        #
        '''
C# >   |   |   |   |   |   AssetTarget -> isFilterAtlas
C# >   |   |   |   |   |   AssetTarget -> FilterModel
C# >   |   |   |   |   |   |   AssetPostProcessor -> isNeedReImport 
C# >   |   |   |   |   |   |   |   AssetPostProcessor -> readCacheInfo
C# >   |   |   |   |   |   AssetTarget -> FilterAnimator
C# >   |   |   |   |   |   AssetTarget -> isFilerBuildInRes
        ''',
        '''
C# >   |   |   |   |   |   AssetTarget -> isFilterAtlas
C# >   |   |   |   |   |   AssetTarget -> FilterModel
C# >   |   |   |   |   |   AssetTarget -> FilterAnimator
C# >   |   |   |   |   |   AssetTarget -> isFilerBuildInRes
C# >   |   |   |   |   |   |   ReplaceShaderTool -> ReplaceBuildInShader
        ''',
        '''
C# >   |   |   |   |   |   AssetTarget -> isFilterAtlas
C# >   |   |   |   |   |   AssetTarget -> FilterModel
C# >   |   |   |   |   |   AssetTarget -> FilterAnimator
C# >   |   |   |   |   |   AssetTarget -> isFilerBuildInRes
        ''',
        '''
C# >   |   |   |   |   AssetTarget -> Merge  
C# >   |   |   |   |   |   AssetTarget -> NeedExportStandalone
C# >   |   |   |   |   AssetTarget -> AnalyzeIfDepTreeChanged
C# >   |   |   |   |   |   AssetTarget -> GetDependencies
        ''',
        '''
C# >   |   |   |   AssetTarget -> WriteCache
C# >   |   |   |   |   AssetTarget -> GetHash
C# >   |   |   |   |   |   AssetBundleUtils -> GetFileHash 
C# >   |   |   |   |   |   |   HashUtil -> Get
C# >   |   |   |   |   |   |   |   HashUtil -> ToHexString
C# >   |   |   |   |   AssetTarget -> GetDependencies
        ''',
        '''
C# >   |   |   |   AssetTarget -> WriteCache
C# >   |   |   |   |   AssetTarget -> GetHash
C# >   |   |   |   |   |   AssetBundleUtils -> GetFileHash 
C# >   |   |   |   |   AssetTarget -> GetDependencies
        ''',
        '''
C# >   |   |   |   |   |   AssetTarget -> BeforeExport
C# >   |   |   |   |   |   |   AssetTarget -> BeforeExport
C# >   |   |   |   |   |   |   AssetTarget -> GetRoot
C# >   |   |   |   |   |   |   |   AssetTarget -> GetRoot
        ''',
        # 双行
        '''
C# >   |   |   AssetBundleUtils -> Load
C# >   |   |   |   AssetBundleUtils -> Load
        ''',
        # 单行 - 循环或者递归
        '''
C# >   |   |   |   |   |   |   |   |   FileCache -> .ctor 
        ''',
        '''
C# >   |   |   |   |   |   |   AssetTarget -> ContainsDepend 
        ''',
        '''
C# >   |   |   |   |   AssetTarget -> BeforeExport
        ''',
        '''
C# >   |   |   |   |   |   AssetTarget -> GetRoot
        ''',
        '''
C# >   |   |   |   |   |   AssetTarget -> GetDependencies
        ''',

        '''
C# >   |   |   |   |   |   |   |   AssetTarget -> RemoveDependParent 
        ''',
        '''
C# >   |   |   |   |   |   |   Empty4Raycast -> .ctor
        ''',
        '''
C# >   |   |   |   |   |   |   |   |   |   |   AssetDanshariWatcher -> OnPostprocessAllAssets
        ''',
    ]

    logAnalyse_.analyseLogByPatterns(
        "/disk/file/C#Temp/A/AssetsBundle_log",
        "/disk/file/C#Temp/A/AssetsBundle_log_test",
        _patternList
    )


if __name__ == '__main__':
    from utils import pyServiceUtils

    _svr = pyServiceUtils.getSubSvr(__file__)
    doAssetBundleLogAnalyse(_svr)
