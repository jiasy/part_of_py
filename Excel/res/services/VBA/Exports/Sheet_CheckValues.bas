' 各表之间的 ID 引用是否存在的校验
Sub CheckGameGuideSteps()
    Const dataBeginRow As Long = 6
    Const titleRow As Long = 2
    Dim result As Boolean
    Dim stepGroupIdValues As Variant

    Dim wsGuide As Worksheet:Set wsGuide = ActiveWorkbook.Sheets("GameGuide")
    Dim wsGroup As Worksheet:Set wsGroup = ActiveWorkbook.Sheets("GameGuideGroup")
    Dim wsStep As Worksheet:Set wsStep = ActiveWorkbook.Sheets("GameGuideStep")

    stepGroupIdValues = getColumnValueArray(wsStep, titleRow, "GroupId" , dataBeginRow)
    Dim groupIdValues As Variant
    groupIdValues = getColumnValueArray(wsGroup, titleRow, "Id" , dataBeginRow)
    result = CheckValues(stepGroupIdValues,groupIdValues,"GameGuideStep - GroupId : ")
    If Not result Then
     Exit Sub
    End If
    Dim groupConfIdValues As Variant
    groupConfIdValues = getColumnValueArray(wsGroup, titleRow, "ConfId" , dataBeginRow)
    Dim guideIdValues As Variant
    guideIdValues = getColumnValueArray(wsGuide, titleRow, "Id" , dataBeginRow)
    result = CheckValues(groupConfIdValues,guideIdValues,"GameGuideGroup - ConfId : ")
    If Not result Then
     Exit Sub
    End If
    MsgBox "Success"
End Sub

' fromValues 的值在 targetValues 中是否出现过
Function CheckValues(fromValues As Variant,targetValues As Variant,tipStr As String) As Boolean
    Dim value As Variant
    Dim matchResult As Variant
    Dim notFoundList As String
    notFoundList = ""
    For Each value In fromValues
        matchResult = IsValueInArr(value, targetValues)
        If matchResult = False Then
            notFoundList = notFoundList & value & ", "
        End If
    Next value
    If Len(notFoundList) > 0 Then
        notFoundList = Left(notFoundList, Len(notFoundList) - 2)
        MsgBox tipStr & " Not found " & notFoundList
        CheckValues = False
    Else
        CheckValues = True
    End If
End Function
