' ���Ҳ�ڼ�λ��ʼ�з֣�����λ������һ�����ص�����Ϊ��
' Dim parts As Variant:parts = SplitFromRightPos("123456789", 4)
' parts(0) -> 12345 parts(1) -> 6789
Function SplitFromRightPos(Byval splitTargetNum As Long, rightPos As Integer) As Variant
    Dim numStr As String
    numStr = CStr(splitTargetNum)
    Dim firstPart As String ' ��ʼ����������ֵ
    Dim lastPart As String
    If Len(numStr) < rightPos Then ' ������ֳ����Ƿ����Էָ�
        firstPart = "0" ' ���ֳ��Ȳ���ʱ���õ�һ������Ϊ0
        lastPart = numStr
    Else
        firstPart = Left(numStr, Len(numStr) - rightPos) ' �ָ����������
        lastPart = Right(numStr, rightPos)
    End If
    SplitFromRightPos = Array(CLng(firstPart), CLng(lastPart)) ' ���ָ���ַ���ת��������
End Function


' �滻��������
' Debug.Print ReplaceLeftStr("123456789", 3, "***")
' ���ӦΪ "***789"
Function ReplaceLeftStr(Byval str As String, Byval numChars As Integer, Byval replacementStr As String) As String
    If Len(str) > numChars Then
        str = replacementStr & Right(str, numChars)
    End If
    ReplaceLeftStr = str
End Function