Sub MoveWindowToSelection()
    Application.Goto Reference:=Selection, Scroll:=True ' �����ڶ�λ��ѡ�����Ŀ
End Sub

Sub CreateShapeWithText()
    ' From Python
    Dim text As String : text = ReadFromFile() ' ��ȡ�ı�����
    Dim lines() As String : lines = Split(text, "&&")
    ' ��һ�� �������
    Dim firstLine As String : firstLine = lines(0)' �е�һ�У��ҳ�ȫ�ֲ���
    Dim firstLines() As String : firstLines = Split(firstLine, "&") ' ��ȫ�ֲ���
    Dim beginX As Integer : beginX = CDbl(firstLines(0))
    Dim fromHeight As Double : fromHeight = CDbl(firstLines(1))
    Dim repeatCount As Integer : repeatCount = CDbl(firstLines(2))
    ' ������״
    Dim widthOffset As Double : widthOffset = 0
    Dim buffer As Double: buffer = 10
    Dim blockHeight As Double : blockHeight = 0 ' ��ǰ��һ��ĸ�
    For ID = 1 To UBound(lines)
        Dim parameters() As String:parameters = Split(lines(ID), "&") ' ��������
        Dim newWidth As Double : newWidth = 0' ÿһ�еĿ�
        Dim lineHeight As Double:lineHeight = parameters(9) + buffer ' �и�
        For i = 0 To UBound(parameters) Step repeatCount
            ' ����������״
            Dim shape As shape
            Set shape = ActiveSheet.Shapes.AddShape(msoShapeRoundedRectangle, beginX + newWidth + buffer, fromHeight + buffer + blockHeight, 100, 100)
            ' ������״��ʽ���ı�
            shape.TextFrame2.TextRange.Font.Size = parameters(i + 9) ' �ֺ�
            shape.TextFrame2.TextRange.text = parameters(i + 11) ' �ı�����
            shape.TextFrame2.VerticalAnchor = msoAnchorMiddle
            shape.TextFrame.AutoSize = True
            ' ������״��ʽ���ı�
            shape.Fill.ForeColor.RGB = RGB(parameters(i + 3), parameters(i + 4), parameters(i + 5)) ' ���������ɫ���˴�ʹ�ú�ɫ��Ϊʾ��
            shape.Line.ForeColor.RGB = RGB(parameters(i + 6), parameters(i + 7), parameters(i + 8)) ' ���������ɫ���˴�ʹ����ɫ��Ϊʾ��
            shape.Line.Weight = parameters(i + 10) ' ������߿��
            shape.Adjustments.Item(1) = 0.1 ' Բ�ǽ�
            ' Ϊ������״����һ�����ı���
            With shape.TextFrame2.TextRange
                With .Font.Fill ' �����ı���ɫ���˴�ʹ����ɫ��Ϊʾ��
                    .Visible = msoTrue
                    .ForeColor.RGB = RGB(parameters(i), parameters(i + 1), parameters(i + 2)) ' ������ɫ
                End With
            End With
            ' ������״��С�Զ��������հ�
            shape.Width = shape.Width + buffer
            shape.Height = lineHeight
            newWidth = newWidth + shape.Width
            ' �����״�Ա㴴����һ����״
            Set shape = Nothing
        Next i
        blockHeight = blockHeight + lineHeight
        widthOffset = Application.Max(widthOffset, newWidth)
    Next ID
    ' ����ռλ�������԰�����
    Set wrapShape = ActiveSheet.Shapes.AddShape(msoShapeRoundedRectangle, 0, fromHeight + lineHeight, buffer + widthOffset + buffer, buffer + blockHeight + buffer)
    wrapShape.Fill.ForeColor.RGB = RGB(firstLines(3), firstLines(4), firstLines(5))
    wrapShape.Adjustments.Item(1) = 0.03 'Բ�ǽ�
    wrapShape.ZOrder msoSendToBack
    fromHeight = fromHeight + buffer + blockHeight + buffer
    Dim textToWrite As String
    textToWrite = "" & fromHeight
    Call WriteToFile(textToWrite)
End Sub

Sub MergeCellsToFitText()
    ' From Python
    Dim text As String : text = ReadFromFile() ' ��ȡ�ı�����
    Dim lines() As String : lines = Split(text, "&&") ' ÿһ��
    ' ��һ�е��������
    Dim firstLine As String : firstLine = lines(0) ' ��һ��
    Dim firstLines() As String : firstLines = Split(firstLine, "&") ' ��ȫ�ֲ���
    Dim beginX As Integer : beginX = CDbl(firstLines(0)) ' ��ʼλ��
    Dim fromHeight As Double : fromHeight = CDbl(firstLines(1)) ' ��ʼ��
    Dim repeatCount As Integer : repeatCount = CDbl(firstLines(2))  ' �����ĸ���
    ' ����ʱ����
    Dim lineCount As Integer : lineCount = 0 ' ����
    Dim lineMergeCount As Integer : lineMergeCount = 1 ' �ϲ����ڼ���

    For ID = 1 To UBound(lines)
        Dim parameters() As String : parameters = Split(lines(ID), "&") ' ��������
        lineMergeCount = 1
        For i = 0 To UBound(parameters) Step repeatCount
            Dim cell As range
            Set cell = Cells(fromHeight + lineCount, beginX + lineMergeCount)
            cell.Font.Name = "Consolas"
            cell.Font.Size = 12
            cell.NumberFormat = "@"  ' @ ��ʾ���ı���ʽ
            cell.Value = parameters(i + 6)
            cell.Interior.Color = RGB(parameters(i + 3), parameters(i + 4), parameters(i + 5)) ' ���õ�Ԫ��ı�����ɫ
            cell.Font.Color = RGB(parameters(i + 0), parameters(i + 1), parameters(i + 2)) ' ���õ�Ԫ�����ֵ���ɫ
            Dim pixelWidth As Double : pixelWidth = GetTxtLen(parameters(i + 6)) ' �����ı������س���
            Dim mergeCount As Integer : mergeCount = Ceiling(pixelWidth / 16)
            If mergeCount = 0 Then
                mergeCount = 1
            End If
            range(cell, cell.Offset(0, mergeCount - 1)).Merge ' �ϲ���Ҫ�ĸ��ӷ�Χ
            lineMergeCount = lineMergeCount + mergeCount
            cell.Value = parameters(i + 6) ' �ںϲ���ĵ�Ԫ���ڲ����ı�
        Next i
        lineCount = lineCount + 1
    Next ID

    Dim textToWrite As String
    textToWrite = mergeCount & ""
    Call WriteToFile(textToWrite)
End Sub
' ����ȡ��
Function Ceiling(Byval x As Double) As Integer
    If x > Int(x) Then
        Ceiling = Int(x) + 1
    Else
        Ceiling = Int(x)
    End If
End Function
' ��ȡ�ı�����
Function GetTxtLen(text As String)
    ' �����������ؿ�Ⱥ�Ӣ�����ַ��ŵ����ؿ��
    Dim chinesePixelWidth As Double : chinesePixelWidth = 12 ' �������ؿ��
    Dim englishPixelWidth As Double : englishPixelWidth = 7 ' Ӣ�����ַ��ŵ����ؿ��
    ' Ӣ�ĺ����ĸ���
    Dim count As Integer : count = 0
    Dim countC As Integer : countC = 0
    Dim i As Integer
    For i = 1 To Len(text)
        Dim char As String : char = Mid(text, i, 1)
        If (Asc(char) >= 32 And Asc(char) <= 126) Or char = "_" Then
            count = count + 1
        Else
            countC = countC + 1
        End If
    Next i
    GetTxtLen = count * englishPixelWidth + countC * chinesePixelWidth
End Function
