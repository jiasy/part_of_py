' 从右侧第几位开始切分，不够位数，第一个返回的数字为零
' Dim parts As Variant:parts = SplitFromRightPos("123456789", 4)
' parts(0) -> 12345 parts(1) -> 6789
Function SplitFromRightPos(Byval splitTargetNum As Long, rightPos As Integer) As Variant
    Dim numStr As String
    numStr = CStr(splitTargetNum)
    Dim firstPart As String ' 初始化两部分数值
    Dim lastPart As String
    If Len(numStr) < rightPos Then ' 检查数字长度是否足以分割
        firstPart = "0" ' 数字长度不够时设置第一个部分为0
        lastPart = numStr
    Else
        firstPart = Left(numStr, Len(numStr) - rightPos) ' 分割成两个部分
        lastPart = Right(numStr, rightPos)
    End If
    SplitFromRightPos = Array(CLng(firstPart), CLng(lastPart)) ' 将分割的字符串转换回数字
End Function


' 替换并输出结果
' Debug.Print ReplaceLeftStr("123456789", 3, "***")
' 输出应为 "***789"
Function ReplaceLeftStr(Byval str As String, Byval numChars As Integer, Byval replacementStr As String) As String
    If Len(str) > numChars Then
        str = replacementStr & Right(str, numChars)
    End If
    ReplaceLeftStr = str
End Function