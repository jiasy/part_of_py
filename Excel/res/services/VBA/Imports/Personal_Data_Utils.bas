' ������һ���в��� �ֶ��� Ϊ ����ֵ �� Cell
' Dim cell As range: Set cell = FindCellInRowByTitle(����ҳ��, ����, ����������, �к�)
Function FindCellInRowByTitle(ws As Worksheet, titleRow As Long, title As String, dataRow As Long) As range
    Dim id As Long
    Dim lastColumn As Long
    lastColumn = ws.Cells(titleRow, ws.Columns.count).End(xlToLeft).Column
    For id = 1 To lastColumn ' �����У�Ѱ��ƥ�����ĵ�Ԫ��
        Dim value As Variant: value = ws.Cells(titleRow, id).value
        If value = title Then
            Set FindCellInRowByTitle = ws.Cells(dataRow, id) ' �ҵ�ƥ��������ڵĵ�Ԫ�񣬷��������Ԫ�����
         Exit Function
        End If
    Next id
    Set FindCellInRowByTitle = Nothing
End Function

' ws �� title ���ڵ��� ��ֵ ���� searchValue �� �� ���ɵ�����
Function getRowArrWithSameValueInTitle(ws As Worksheet, titleRow As Long, title As String, dataRow As Long, searchValue As Variant) As Variant
    Dim groupCol As Long: groupCol = getColumnArrayByTitle(wsGroup, titleRow, Array(title))(0) ' ������
    Dim matchedRows() As Long
    Dim rowCount As Long: rowCount = 0
    Dim currentRow As Long
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.count, groupCol).End(xlUp).Row ' ��λ���һ��

    ' ��ָ������ѭ�����Ҿ����ض�ֵ����
    For currentRow = dataRow To lastRow
        If StrComp(ws.Cells(currentRow, groupCol).value, searchValue, vbTextCompare) = 0 Then
            ReDim Preserve matchedRows(rowCount)
            matchedRows(rowCount) = currentRow
            rowCount = rowCount + 1
        End If
    Next currentRow

    ' ����ҵ�ƥ���У��������飬���򷵻ؿ�����
    If rowCount > 0 Then
        ReDim Preserve matchedRows(LBound(matchedRows) To UBound(matchedRows))
    Else
        ReDim matchedRows(0)
    End If

    getRowArrWithSameValueInTitle = matchedRows
End Function

' ws �� ��ȡֵ��ͬ�� Id ���ڵĸ���
Function getCellArrWithSameValueInTitle(ws As Worksheet, titleRow As Long, title As String, dataRow As Long, value As Long) As range()
    Dim targetCol As Long
    Dim lastRow As Long
    Dim rId As Long
    Dim tempArray() As Range
    Dim currentCell As Range
    Dim cellCount As Long: cellCount = 0
    targetCol = getColumn(ws, titleRow, Array(title))(0) ' �ҵ��б��
    lastRow = ws.Cells(ws.Rows.Count, targetCol).End(xlUp).Row ' �ҵ��е����һ��
    For rId = dataRow To lastRow ' ������ dataRow �� lastRow �ĵ�Ԫ��
        Set currentCell = ws.Cells(rId, targetCol)
        If IsNumeric(currentCell.Value) Then
            If currentCell.Value = value Then ' ���ֵ�Ƿ����id
                ReDim Preserve tempArray(cellCount) ' ������ϣ���ӵ�����tempArray��
                Set tempArray(cellCount) = currentCell
                cellCount = cellCount + 1
            End If
        End If
    Next rId
    getCellArrWithSameValueInTitle = tempArray ' ����ƥ�䵥Ԫ�������
End Function

' �� targetSheetName Sheet�ϣ��к�Ϊ titleRow �������ҵ�ֵΪ title ���У��� dataBeginRow ������ȡ���ݼ�¼������
' Dim columnValues As Variant:columnValues = getColumnValueArray(ActiveSheet, 2, "Id", 6)
Function getColumnValueArray((ws As Worksheet, titleRow As Long, title As String, dataRow As Long) As Variant
    ' ���巵��ֵ
    Dim backArray() As Variant
    ReDim backArray(0 To 0)
    ' ȡĿ����
    Dim targetRNG As range
    Set targetRNG = ws.Rows(titleRow).Find(title, LookIn:=xlValues, LookAt:=xlWhole) ' һ���и���
    If targetRNG Is Nothing Then ' û���������
        MsgBox "title " & title & " Not found."
        getColumnValueArray = Array() ' ���ؿ�����
     Exit Function
    End If
    ' ��ֵ
    Dim idx As Long:idx = -1
    Dim cell As range
    Dim cellValue As Variant
    For Each cell In ws.Range(ws.Cells(dataRow, targetRNG.Column), ws.Cells(ws.Rows.Count, targetRNG.Column)).Cells
        cellValue = cell.Value
        If Not IsEmpty(cellValue) Then ' ��¼�ǿ�ֵ
            idx = idx + 1
            ReDim Preserve backArray(0 To idx)
            backArray(idx) = cellValue
        End If
    Next cell
    ' ����ֵ
    If idx = -1 Then
        getColumnValueArray = Array()
    Else
        getColumnValueArray = backArray
    End If
End Function

' ��ȡָ�����У�����ָ��ֵ���к�
' Dim columnNumArray As Variant:columnNumArray = getColumnArrayByTitle(ActiveSheet, 2, Array("Id"))
Function getColumnArrayByTitle(ws As Worksheet, titleRow As Long, valueArray As Variant) As Variant
    Dim backArray() As Variant ' ���ص��Ǹ�����
    Dim count As Long: count = 0 
    Dim cellValue As String,cell As range,idx As Long ' ѭ���ñ���
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