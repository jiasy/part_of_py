' valueToFind ֵ�Ƿ��� arr ֮��
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
    If Not element Is Nothing Then ' ֻ�е� `element` ���ǿյ�ʱ��ż���
        If Not IsArrayInitialized(arr) Then
            ReDim arr(0) ' ��ʼ�����鲢��ӵ�һ��Ԫ��
            Set arr(0) = element
        Else
            ReDim Preserve arr(UBound(arr) + 1) ' ��������ѳ�ʼ�����������Ԫ�ص�����ĩβ
            Set arr(UBound(arr)) = element
        End If
    End If
    AddToArrEnd = arr ' ���ظ��¹�������
End Function

Function AddToArrBegin(arr As Variant, element As Variant) As Variant
    Dim tempArr() As Variant
    Dim id As Long
    If Not element Is Nothing Then ' ֻ�е� `element` ���ǿյ�ʱ��ż���
        If Not IsArrayInitialized(arr) Then
            ReDim tempArr(0) ' �������δ��ʼ�������ʼ�����鲢��ӵ�һ��Ԫ��
            tempArr(0) = element
        Else
            ReDim tempArr(UBound(arr) + 1) ' ��������ѳ�ʼ�������������鲢���Ԫ������ʼ��Ȼ����ʣ�ಿ��
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
    If Not IsArrayInitialized(arr) Or UBound(arr) = LBound(arr) Then ' ��������Ƿ�δ��ʼ�����������һ��Ԫ��
        RemoveArrFirst = arr ' ֱ�ӷ���ԭ����
     Exit Function
    End If
    ReDim tempArr(LBound(arr) To UBound(arr) - 1) ' ��ʼ����ʱ�������ڴ洢���
    For id = LBound(arr) + 1 To UBound(arr) ' ��ԭ����Ԫ�شӵڶ�����ʼ���Ƶ���ʱ����
        tempArr(id - 1) = arr(id)
    Next id
    RemoveArrFirst = tempArr ' �����޸ĺ������
End Function

Function RemoveArrLast(arr As Variant) As Variant
    If Not IsArrayInitialized(arr) Or UBound(arr) = LBound(arr) Then ' ��������Ƿ�δ��ʼ�����������һ��Ԫ��
        RemoveArrLast = arr ' ֱ�ӷ���ԭ����
     Exit Function
    End If
    ReDim Preserve arr(LBound(arr) To UBound(arr) - 1) ' ����ԭ�����С���Ƴ����һ��Ԫ��
    RemoveArrLast = arr ' �����޸ĺ������
End Function

Function IsArrayInitialized(arr As Variant) As Boolean
    On Error Resume Next
    IsArrayInitialized = IsArray(arr) And Not IsError(LBound(arr, 1)) And LBound(arr, 1) <= UBound(arr, 1)
    On Error Goto 0
End Function