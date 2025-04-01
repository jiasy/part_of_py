Const titleRow As Long = 2
' 表的字段太多，类型所需的参数不同，导致表特别长，比较难看
' 当点击类型时，将这个类型相关的参数提前
Private Sub Worksheet_SelectionChange(Byval Target As Excel.Range)
    Dim watchValue As String: watchValue = "Type"
    Dim cellToCheck As range
    If Target.Cells.CountLarge = 1 And Target.Row >= 6 Then '如果选中的是单个单元格而不是多个单元格
        Set cellToCheck = Me.Cells(titleRow, Target.Column) '设置要检查的单元格为同一列的第titleRow行单元格
        If cellToCheck.Value = watchValue Then '检查这个单元格的值是否符合条件
            Dim selectedCell As range
            Set selectedCell = Target(1, 1)
            ' 符合条件的，按照当前值只显示当前值所需要的字段
            HideOtherColumnsBasedOnValuesNextToSelectedCell selectedCell.Value, Target
        Else
            ActiveSheet.Columns.Hidden = False ' 不符合条件，显示所有列
        End If
    End If
End Sub

'不同类型关联的字段不同
Function GetTypeUseParamList(value As Long) As Variant
    Select Case value
     Case 1 '点击UI
        GetTypeUseParamList = Array("ResPath", "LayerFrame", "Widget","LightGroup","WidgetClick")
     Case 2 '对话
        GetTypeUseParamList = Array("DialogId")
     Case 3 '跳转
        GetTypeUseParamList = Array("OpenFunc")
     Case 4 '建筑、障碍-本身
        GetTypeUseParamList = Array("BuildingId","BlockId")
     Case 5 '建筑、障碍-气泡
        GetTypeUseParamList = Array("BuildingId","BlockId")
     Case 6 '点击引导任意处继续
        GetTypeUseParamList = Array("ResPath", "LayerFrame", "Widget","LightGroup","WidgetClick")
     Case 7 '建筑、障碍-弹出框
        GetTypeUseParamList = Array("BuildingId","BlockId")
     Case 8 '拖动合成
        GetTypeUseParamList = Array("SoldierId")
     Case 9 'Behavior Tree
        GetTypeUseParamList = Array("BehaviorId")
     Case 10 '选择迷雾
        GetTypeUseParamList = Array("SmokeId")
     Case 11 '清理迷雾
        GetTypeUseParamList = Array("SmokeId")
     Case 12 '等待战斗结束
        GetTypeUseParamList = Array()
     Case 13 'UI->引导
        GetTypeUseParamList = Array("CustomEvent")
     Case 14 '建筑、障碍-放置框
        GetTypeUseParamList = Array("BuildingId","BlockId")
     Case 15 '建筑、障碍-引导查看
        GetTypeUseParamList = Array("BuildingId","BlockId")
     Case 16 '引导->UI
        GetTypeUseParamList = Array("ResPath","customFunc")
     Case 17 '震屏
        GetTypeUseParamList = Array("ArrayParam")
     Case Else
        GetTypeUseParamList = Array()
    End Select
End Function

' 在选中的单元格之后，隐藏所有列并仅显示数组中指定的列
Sub HideOtherColumnsBasedOnValuesNextToSelectedCell(cellValue As Long, selectedCell As range)
    Dim Worksheet As Worksheet: Set Worksheet = selectedCell.Parent
    Dim valuesList As Variant: valuesList = GetTypeUseParamList(cellValue) ' 获取标题值
    Dim columnIndexesToShow As Variant: columnIndexesToShow = getColumnArrayByTitle(titleRow, valuesList) ' 获取标题值所在的列
    Dim lastColumn As Long: lastColumn = Worksheet.UsedRange.Columns(Worksheet.UsedRange.Columns.Count).Column ' 获取当前使用的最后一列
    Dim idx As Integer ' 从所选格开始，一直隐藏到最后一列
    For idx = selectedCell.Column + 1 To lastColumn
        Worksheet.Columns(idx).Hidden = True
    Next idx 
    ' 只有指定标题值的才显示
    For idx = LBound(columnIndexesToShow) To UBound(columnIndexesToShow)
        If columnIndexesToShow(idx) > selectedCell.Column Then
            Worksheet.Columns(columnIndexesToShow(idx)).Hidden = False
        End If
    Next idx
End Sub

