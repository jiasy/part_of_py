' valueToFind 值是否在 arr 之内
' Dim isIn As Boolean:isIn = IsValueInArr(2, Array(2,4))
Function IsValueInArr(valueToFind As Variant, arr As Variant) As Boolean
    Dim idx As Long
    For idx = LBound(arr) To UBound(arr)
        If arr(idx) = valueToFind Then
            IsValueInArr = True
         Exit Function
        End If
    Next idx
    IsValueInArr = False
End Function

Function AddToArrEnd(arr As Variant, element As Variant) As Variant
    If Not element Is Nothing Then ' 只有当 `element` 不是空的时候才继续
        If Not IsArrayInitialized(arr) Then
            ReDim arr(0) ' 初始化数组并添加第一个元素
            Set arr(0) = element
        Else
            ReDim Preserve arr(UBound(arr) + 1) ' 如果数组已初始化，则添加新元素到数组末尾
            Set arr(UBound(arr)) = element
        End If
    End If
    AddToArrEnd = arr ' 返回更新过的数组
End Function

Function AddToArrBegin(arr As Variant, element As Variant) As Variant
    Dim tempArr() As Variant
    Dim id As Long
    If Not element Is Nothing Then ' 只有当 `element` 不是空的时候才继续
        If Not IsArrayInitialized(arr) Then
            ReDim tempArr(0) ' 如果数组未初始化，则初始化数组并添加第一个元素
            tempArr(0) = element
        Else
            ReDim tempArr(UBound(arr) + 1) ' 如果数组已初始化，创建新数组并添加元素至开始，然后复制剩余部分
            tempArr(LBound(tempArr)) = element
            For id = LBound(arr) To UBound(arr)
                tempArr(id + 1) = arr(id)
            Next id
        End If
    End If
    AddToArrBegin = tempArr
End Function

Function RemoveArrFirst(arr As Variant) As Variant
    Dim id As Long
    If Not IsArrayInitialized(arr) Or UBound(arr) = LBound(arr) Then ' 检查数组是否未初始化或数组仅有一个元素
        RemoveArrFirst = arr ' 直接返回原数组
     Exit Function
    End If
    ReDim tempArr(LBound(arr) To UBound(arr) - 1) ' 初始化临时数组用于存储结果
    For id = LBound(arr) + 1 To UBound(arr) ' 将原数组元素从第二个开始复制到临时数组
        tempArr(id - 1) = arr(id)
    Next id
    RemoveArrFirst = tempArr ' 返回修改后的数组
End Function

Function RemoveArrLast(arr As Variant) As Variant
    If Not IsArrayInitialized(arr) Or UBound(arr) = LBound(arr) Then ' 检查数组是否未初始化或数组仅有一个元素
        RemoveArrLast = arr ' 直接返回原数组
     Exit Function
    End If
    ReDim Preserve arr(LBound(arr) To UBound(arr) - 1) ' 缩减原数组大小，移除最后一个元素
    RemoveArrLast = arr ' 返回修改后的数组
End Function

Function IsArrayInitialized(arr As Variant) As Boolean
    On Error Resume Next
    IsArrayInitialized = IsArray(arr) And Not IsError(LBound(arr, 1)) And LBound(arr, 1) <= UBound(arr, 1)
    On Error Goto 0
End Function
