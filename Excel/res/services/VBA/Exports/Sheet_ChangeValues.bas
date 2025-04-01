' 要定义到 模块 里
'Type ArraysHolder
'    guide_mutexId_cell_arr() As range
'    guide_relationId_cell_arr() As range
'    guide_preId_cell_arr() As range
'    group_id_cell_arr() As range
'    group_guide_id_cell_arr() As range
'    step_id_cell_arr() As range
'    step_group_id_cell_arr() As range
'    step_guide_id_cell_arr() As range
'End Type
' 向后窜一位
Sub push()
    ' 初始化变量
    Dim titleRow As Long: titleRow = 2
    Dim dataRow As Long: dataRow = 6

    Dim selectedColumn As Long
    selectedColumn = Selection.Column

    ' 判断当前的Sheet名称是否为"GameGuide"
    If ActiveSheet.Name <> "GameGuide" Then
     Exit Sub
    End If

    ' 判断当前是否选择了1个单元格
    If Selection.Cells.count <> 1 Then
     Exit Sub
    End If

    ' 获取该列第二行的单元格
    If Selection.Worksheet.Cells(titleRow, selectedColumn).Value <> "Id" Then
     Exit Sub
    End If

    ' 所选格子的值
    Dim selectedValue As Variant
    selectedValue = Selection.Value

    ' 弹出一个确认框
    Dim continueResponse As VbMsgBoxResult
    continueResponse = MsgBox( "确认 Guide " & Selection(1).value & " 以及大于它的 Id + 1 ?", vbQuestion + vbYesNo, "确认")
    If continueResponse = vbNo Then
        MsgBox "已退出", vbInformation
    Else
        Dim lastRow As Long: lastRow = Selection.Worksheet.Cells(Selection.Worksheet.Rows.Count, selectedColumn).End(xlUp).Row
        Dim rId As Long
        Dim cellsToChange As New Collection ' 收集要变更的单元格
        Dim currentCell As Range
        For rId = dataRow To lastRow ' 聚集所有大于或等于selectedValue的单元格用以倒序排序
            Set currentCell = Selection.Worksheet.Cells(rId, selectedColumn)
            If IsNumeric(currentCell.Value) Then
                If currentCell.Value >= selectedValue Then
                    cellsToChange.Add currentCell ' 将符合条件的单元格添加到cellsToChange集合中
                End If
            End If
        Next rId
        Debug.Print "排序完毕"
        Dim idx As Long ' 倒序处理cellsToChange集合中的单元格
        For idx = cellsToChange.Count To 1 Step -1
            Debug.Print "进行中 : " & idx & " / " & cellsToChange.Count
            Set currentCell = cellsToChange(idx)
            Dim groupAndStepHolder As ArraysHolder: groupAndStepHolder = walkSheet(currentCell.Value, titleRow, dataRow)
            Call changeGroupStepHolder(groupAndStepHolder, currentCell.Value + 1) ' 对groupAndStepHolder进行更新操作
            currentCell.Value = currentCell.Value + 1 ' 更新单元格的值
        Next idx
    End If
End Sub

' 交换
Sub swapping()
    ' 初始化变量
    Dim titleRow As Long: titleRow = 2
    Dim dataRow As Long: dataRow = 6
    ' 判断当前的Sheet名称是否为"GameGuide"
    If ActiveSheet.Name <> "GameGuide" Then
     Exit Sub
    End If
    ' 判断当前是否选择了两个单元格
    If Selection.Cells.count <> 2 Then
     Exit Sub
    End If

    ' 获取该列第二行的单元格
    If Selection.Worksheet.Cells(titleRow, Selection.Column).Value <> "Id" Then
     Exit Sub
    End If

    Dim cell As range
    Dim id As Integer
    Dim cellValues() As Variant
    ReDim cellValues(1 To 2)

    id = 1 ' 为两个单元格对象设置数组
    For Each cell In Selection ' 循环遍历选定的每个单元格，并检查是否为空
        If IsEmpty(cell.value) Then
         Exit Sub ' 如果有任何一个单元格为空，则退出
        Else
            Set cellValues(id) = cell ' 保存单元格对象而不是值
            id = id + 1
        End If
    Next cell

    ' 弹出一个确认框
    Dim continueResponse As VbMsgBoxResult
    continueResponse = MsgBox( "确认 Guide " & cellValues(1).value & " 和 " & cellValues(2).value & " 交换？", vbQuestion + vbYesNo, "确认")
    If continueResponse = vbNo Then
        MsgBox "已退出", vbInformation
    Else
        ' 确认继续后，调用walkSheet函数
        Dim fromValue As Long: fromValue = CLng(cellValues(1))
        Dim toValue As Long: toValue = CLng(cellValues(2))
        Dim groupAndStepHolderFrom As ArraysHolder: groupAndStepHolderFrom = walkSheet(fromValue, titleRow,dataRow)
        Dim groupAndStepHolderTo As ArraysHolder: groupAndStepHolderTo = walkSheet(toValue, titleRow,dataRow)
        Call changeGroupStepHolder(groupAndStepHolderFrom, toValue)
        Call changeGroupStepHolder(groupAndStepHolderTo, fromValue)
        cellValues(1).value = toValue
        cellValues(2).value = fromValue
    End If
End Sub

Sub UpdateCellValues(Byref cellArray As Variant, Byval replaceLength As Long, Byval targetValue As Long)
    Dim idx As Long
    For idx = LBound(cellArray) To UBound(cellArray)
        Dim cell As Range: Set cell = cellArray(idx)
        Dim currentIdStr As String: currentIdStr = CStr(cell.Value)
        currentIdStr = ReplaceLeftStr(currentIdStr, replaceLength, CStr(targetValue))
        cell.Value = CLng(currentIdStr)
    Next idx
End Sub

' 修改 GuideId 下的 Group 和 Step 的 Id 的 Cell
Sub changeGroupStepHolder(holder As ArraysHolder, targetValue As Long)
    Dim guide_mutexId_cell_arr As Variant: guide_mutexId_cell_arr = holder.guide_mutexId_cell_arr
    Dim guide_relationId_cell_arr As Variant: guide_relationId_cell_arr = holder.guide_relationId_cell_arr
    Dim guide_preId_cell_arr As Variant: guide_preId_cell_arr = holder.guide_preId_cell_arr
    Dim group_id_cell_arr As Variant: group_id_cell_arr = holder.group_id_cell_arr
    Dim group_guide_id_cell_arr As Variant: group_guide_id_cell_arr = holder.group_guide_id_cell_arr
    Dim step_id_cell_arr As Variant: step_id_cell_arr = holder.step_id_cell_arr
    Dim step_group_id_cell_arr As Variant: step_group_id_cell_arr = holder.step_group_id_cell_arr
    Dim step_guide_id_cell_arr As Variant: step_guide_id_cell_arr = holder.step_guide_id_cell_arr
    Call UpdateCellValues(guide_mutexId_cell_arr, 0, targetValue)
    Call UpdateCellValues(guide_relationId_cell_arr, 0, targetValue)
    Call UpdateCellValues(guide_preId_cell_arr, 0, targetValue)
    Call UpdateCellValues(group_id_cell_arr, 2, targetValue)
    Call UpdateCellValues(group_guide_id_cell_arr, 0, targetValue)
    Call UpdateCellValues(step_id_cell_arr, 4, targetValue)
    Call UpdateCellValues(step_group_id_cell_arr, 2, targetValue)
    Call UpdateCellValues(step_guide_id_cell_arr, 0, targetValue)
End Sub

' 获取 GuideId 下的 Group 和 Step 的 Id 的 Cell
Function walkSheet(guideId As Long, titleRow As Long,dataRow As Long) As ArraysHolder
    Debug.Print guideId
    Dim wsGuide As Worksheet: Set wsGuide = ActiveWorkbook.Sheets("GameGuide")
    Dim tempGuideMutexIdArr() As range:tempGuideMutexIdArr = getCellArrWithSameValueInTitle(wsGuide, titleRow, "MutexId", dataRow, guideId)
    Dim tempGuideRelationIdArr() As range:tempGuideRelationIdArr = getCellArrWithSameValueInTitle(wsGuide, titleRow, "RelationId", dataRow, guideId)
    Dim tempGuidePreIdArr() As range:tempGuidePreIdArr = getCellArrWithSameValueInTitle(wsGuide, titleRow, "PreId", dataRow, guideId)

    Dim groupAndStepHolder As ArraysHolder
    Dim tempGroupIdArr() As range
    Dim tempGroupGuideIdArr() As range
    Dim tempStepIdArr() As range
    Dim tempStepGroupIdArr() As range
    Dim tempStepGuideIdArr() As range
    Dim wsGroup As Worksheet: Set wsGroup = ActiveWorkbook.Sheets("GameGuideGroup")
    Dim wsStep As Worksheet: Set wsStep = ActiveWorkbook.Sheets("GameGuideStep")
    Dim groupRows As Variant: groupRows = getRowArrWithSameValueInTitle(wsGroup, titleRow, "ConfId", dataRow, guideId) ' 列数据
    For groupIdx = LBound(groupRows) To UBound(groupRows)
        Dim groupIdCell As range: Set groupIdCell = FindCellInRowByTitle(wsGroup, titleRow, "Id", CLng(groupRows(groupIdx)))
        If Not IsEmpty(groupIdCell.value) Then ' 记录非控值
            tempGroupIdArr = AddToArr(tempGroupIdArr, groupIdCell)
            Dim groupId As Long: groupId = groupIdCell.value
            Debug.Print "    " & groupId
            Dim stepRows As Variant: stepRows = getRowArrWithSameValueInTitle(wsStep, titleRow, "GroupId", dataRow, groupId) ' 列数据
            For stepIdx = LBound(stepRows) To UBound(stepRows)
                Dim stepIdCell As range: Set stepIdCell = FindCellInRowByTitle(wsStep, titleRow, "Id", CLng(stepRows(stepIdx)))
                If Not IsEmpty(stepIdCell.value) Then ' 记录非控值
                    Dim stepId As Long: stepId = stepIdCell.value
                    Debug.Print "        " & stepId
                    tempStepIdArr = AddToArr(tempStepIdArr, stepIdCell)
                End If
                Dim stepGroupIdCell As range: Set stepGroupIdCell = FindCellInRowByTitle(wsStep, titleRow, "GroupId", CLng(stepRows(stepIdx)))
                If Not IsEmpty(stepGroupIdCell.value) Then ' 记录非控值
                    Dim stepGroupId As Long: stepGroupId = stepGroupIdCell.value
                    Debug.Print "        " & stepGroupId
                    tempStepGroupIdArr = AddToArr(tempStepGroupIdArr, stepGroupIdCell)
                End If
                Dim stepGuideIdCell As range: Set stepGuideIdCell = FindCellInRowByTitle(wsStep, titleRow, "GameGuide", CLng(stepRows(stepIdx)))
                If Not IsEmpty(stepGuideIdCell.value) Then ' 记录非控值
                    Dim stepGuideId As Long: stepGuideId = stepGuideIdCell.value
                    Debug.Print "        " & stepGuideId
                    tempStepGuideIdArr = AddToArr(tempStepGuideIdArr, stepGuideIdCell)
                End If
            Next stepIdx
        End If

        Dim groupGuideIdCell As range: Set groupGuideIdCell = FindCellInRowByTitle(wsGroup, titleRow, "ConfId", CLng(groupRows(groupIdx)))
        If Not IsEmpty(groupGuideIdCell.value) Then ' 记录非控值
            tempGroupGuideIdArr = AddToArr(tempGroupGuideIdArr, groupGuideIdCell)
        End If
    Next groupIdx
    groupAndStepHolder.guide_mutexId_cell_arr = tempGuideMutexIdArr
    groupAndStepHolder.guide_relationId_cell_arr = tempGuideRelationIdArr
    groupAndStepHolder.guide_preId_cell_arr = tempGuidePreIdArr
    groupAndStepHolder.group_id_cell_arr = tempGroupIdArr
    groupAndStepHolder.group_guide_id_cell_arr = tempGroupGuideIdArr
    groupAndStepHolder.step_id_cell_arr = tempStepIdArr
    groupAndStepHolder.step_group_id_cell_arr = tempStepGroupIdArr
    groupAndStepHolder.step_guide_id_cell_arr = tempStepGuideIdArr
    walkSheet = groupAndStepHolder
End Function

' 添加到数组末尾的函数，用于确保对象的正确分配
Function AddToArr(arr() As range, element As range) As Variant
    ' 只有当 `element` 不是空的时候才继续
    If Not element Is Nothing Then
        If Not IsArrayInit(arr) Then
            ReDim arr(0) ' 初始化数组并添加第一个元素
            Set arr(0) = element
        Else
            ' 如果数组已初始化，则添加新元素到数组末尾
            ReDim Preserve arr(UBound(arr) + 1)
            Set arr(UBound(arr)) = element
        End If
    End If
    AddToArr = arr ' 返回更新过的数组
End Function

Function IsArrayInit(arr As Variant) As Boolean
    On Error Resume Next
    IsArrayInit = IsArray(arr) And Not IsError(LBound(arr, 1)) And LBound(arr, 1) <= UBound(arr, 1)
    On Error Goto 0
End Function
