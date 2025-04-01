' 导出 不是 Sheet开头 和 ThisWorkbook 的模块
Sub exportPersonalVBAProjectModule()
    Dim VBComp As Object
    For Each VBComp In ThisWorkbook.VBProject.VBComponents ' 检查每个组件
        If Not VBComp.Name Like "Sheet*" And Not VBComp.Name = "ThisWorkbook" Then ' 写入当期那打开的 excel 所在的文件夹
            Call ExportPersonalVBAModule(VBComp.Name, ActiveWorkbook.path & "/Exports/" & VBComp.Name & ".bas")
        End If
    Next VBComp
End Sub
' 导出指定模块到指定位置
Sub ExportPersonalVBAModule(moduleName As String, ExportPath As String)
    Dim VBProj As Object
    Dim VBComp As Object
    Set VBProj = ThisWorkbook.VBProject
    For Each VBComp In VBProj.VBComponents
        If VBComp.Name = moduleName Then
            VBComp.Export ExportPath
            Debug.Print "模块 " & moduleName & " 已导出到 " & ExportPath, vbInformation
        End If
    Next VBComp
End Sub

Sub importPersonVBAModule()
    Dim folderPath As String
    Dim filename As String
    folderPath =  ActiveWorkbook.path & "/Imports/"
    filename = Dir(folderPath & "*.bas") ' 使用Dir函数获取第一个.bas
    While filename <> "" ' 循环遍历文件夹中所有.bas 文件
        Dim moduleName As String
        moduleName = Split(filename, ".bas")(0) ' 使用VBA的Split函数移除.bas扩展名以获取纯模块名
        If moduleName = "VBA_Export_Import" Then
            ' 执行下一次循环
            Goto ContinueLoop
            End If
            Dim module As Object
            On Error Resume Next ' 忽略错误，试图查找同名模块
            Set module = ThisWorkbook.VBProject.VBComponents(moduleName) ' 使用moduleName查找同名模块
            If Not module Is Nothing Then ' 如果找到同名模块，则先将其移除
                ThisWorkbook.VBProject.VBComponents.Remove VBComponent:=module
            End If
            On Error Goto 0 ' 重置错误处理
                ThisWorkbook.VBProject.VBComponents.Import folderPath & filename ' 导入.bas 文件作为模块、VBA自动切后缀
                RenameModule "模块1", moduleName ' 刚创建的模块改名
 ContinueLoop:
                filename = Dir() ' 使用Dir函数获取下一个.bas
            Wend
End Sub

Sub RenameModule(oldModuleName As String, newModuleName As String)
    Dim VBComp As Object
    For Each VBComp In ThisWorkbook.VBProject.VBComponents
        If VBComp.Name = oldModuleName  Then
            VBComp.Name = newModuleName
        End If
    Next VBComp
End Sub
    