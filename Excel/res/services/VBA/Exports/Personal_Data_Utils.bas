' 在这里一行中查找 字段名 为 给定值 的 Cell
' Dim cell As range: Set cell = FindCellInRowByTitle(所在页面, 标题, 标题所在行, 行号)
Function FindCellInRowByTitle(ws As Worksheet, titleRow As Long, title As String, dataRow As Long) As range
    Dim id As Long
    Dim lastColumn As Long
    lastColumn = ws.Cells(titleRow, ws.Columns.count).End(xlToLeft).Column
    For id = 1 To lastColumn ' 遍历列，寻找匹配标题的单元格
        Dim value As Variant: value = ws.Cells(titleRow, id).value
        If value = title Then
            Set FindCellInRowByTitle = ws.Cells(dataRow, id) ' 找到匹配标题所在的单元格，返回这个单元格对象
         Exit Function
        End If
    Next id
    Set FindCellInRowByTitle = Nothing
End Function

' ws 中 title 所在的列 其值 等于 value 的 行 构成的数组
Function getRowArrWithSameValueInTitle(ws As Worksheet, titleRow As Long, title As String, dataRow As Long, value As Variant) As Variant
    Dim targetCol As Long: targetCol = getColumnArrayByTitle(ws, titleRow, Array(title))(0) ' 所在列
    Dim matchedRows() As Long
    Dim rowCount As Long: rowCount = 0
    Dim currentRow As Long
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.count, targetCol).End(xlUp).Row ' 定位最后一行
    ' 在指定列中循环查找具有特定值的行
    For currentRow = dataRow To lastRow
        If StrComp(ws.Cells(currentRow, targetCol).value, value, vbTextCompare) = 0 Then
            ReDim Preserve matchedRows(rowCount)
            matchedRows(rowCount) = currentRow
            rowCount = rowCount + 1
        End If
    Next currentRow
    ' 如果找到匹配行，返回数组，否则返回空数组
    If rowCount > 0 Then
        ReDim Preserve matchedRows(LBound(matchedRows) To UBound(matchedRows))
    Else
        ReDim matchedRows(0)
    End If
    getRowArrWithSameValueInTitle = matchedRows
End Function

' ws 中 提取值相同的 Id 所在的格子
Function getCellArrWithSameValueInTitle(ws As Worksheet, titleRow As Long, title As String, dataRow As Long, value As Long) As range()
    Dim targetCol As Long
    Dim lastRow As Long
    Dim rId As Long
    Dim tempArray() As Range
    Dim currentCell As Range
    Dim cellCount As Long: cellCount = 0
    targetCol = getColumn(ws, titleRow, Array(title))(0) ' 找到列编号
    lastRow = ws.Cells(ws.Rows.Count, targetCol).End(xlUp).Row ' 找到列的最后一行
    For rId = dataRow To lastRow ' 遍历从 dataRow 到 lastRow 的单元格
        Set currentCell = ws.Cells(rId, targetCol)
        If IsNumeric(currentCell.Value) Then
            If currentCell.Value = value Then ' 检查值是否等于id
                ReDim Preserve tempArray(cellCount) ' 如果符合，添加到数组tempArray中
                Set tempArray(cellCount) = currentCell
                cellCount = cellCount + 1
            End If
        End If
    Next rId
    getCellArrWithSameValueInTitle = tempArray ' 返回匹配单元格的数组
End Function

' 从 targetSheetName Sheet上，行号为 titleRow 的行上找到值为 title 的列，从 dataBeginRow 行向下取数据记录成数组
' Dim columnValues As Variant:columnValues = getColumnValueArray(ActiveSheet, 2, "Id", 6)
Function getColumnValueArray((ws As Worksheet, titleRow As Long, title As String, dataRow As Long) As Variant
    ' 定义返回值
    Dim backArray() As Variant
    ReDim backArray(0 To 0)
    ' 取目标列
    Dim targetRNG As range
    Set targetRNG = ws.Rows(titleRow).Find(title, LookIn:=xlValues, LookAt:=xlWhole) ' 一竖列格子
    If targetRNG Is Nothing Then ' 没有这个竖列
        MsgBox "title " & title & " Not found."
        getColumnValueArray = Array() ' 返回空数组
     Exit Function
    End If
    ' 存值
    Dim idx As Long:idx = -1
    Dim cell As range
    Dim cellValue As Variant
    For Each cell In ws.Range(ws.Cells(dataRow, targetRNG.Column), ws.Cells(ws.Rows.Count, targetRNG.Column)).Cells
        cellValue = cell.Value
        If Not IsEmpty(cellValue) Then ' 记录非控值
            idx = idx + 1
            ReDim Preserve backArray(0 To idx)
            backArray(idx) = cellValue
        End If
    Next cell
    ' 返回值
    If idx = -1 Then
        getColumnValueArray = Array()
    Else
        getColumnValueArray = backArray
    End If
End Function

' 获取指定行中，持有指定值的列号
' Dim columnNumArray As Variant:columnNumArray = getColumnArrayByTitle(ActiveSheet, 2, Array("Id"))
Function getColumnArrayByTitle(ws As Worksheet, titleRow As Long, valueArray As Variant) As Variant
    Dim backArray() As Variant ' 返回的那个数组
    Dim count As Long: count = 0 
    Dim cellValue As String,cell As range,idx As Long ' 循环用变量
    For Each cell In ws.Rows(titleRow).Cells
        cellValue = cell.Value
        For idx = LBound(valueArray) To UBound(valueArray)
            If StrComp(cellValue, valueArray(idx), vbTextCompare) = 0 Then
                ReDim Preserve backArray(count)
                backArray(count) = cell.Column
                count = count + 1
             Exit For
            End If
        Next idx
    Next cell
    If count > 0 Then
        ReDim Preserve backArray(LBound(backArray) To count - 1)
    Else
        ReDim backArray(0)
    End If 
    getColumnArrayByTitle = backArray
End Function
