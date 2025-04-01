Sub MoveWindowToSelection()
    Application.Goto Reference:=Selection, Scroll:=True ' 将窗口定位到选择的项目
End Sub

Sub CreateShapeWithText()
    ' From Python
    Dim text As String : text = ReadFromFile() ' 读取文本内容
    Dim lines() As String : lines = Split(text, "&&")
    ' 第一行 特殊参数
    Dim firstLine As String : firstLine = lines(0)' 切第一行，找出全局参数
    Dim firstLines() As String : firstLines = Split(firstLine, "&") ' 切全局参数
    Dim beginX As Integer : beginX = CDbl(firstLines(0))
    Dim fromHeight As Double : fromHeight = CDbl(firstLines(1))
    Dim repeatCount As Integer : repeatCount = CDbl(firstLines(2))
    ' 创建形状
    Dim widthOffset As Double : widthOffset = 0
    Dim buffer As Double: buffer = 10
    Dim blockHeight As Double : blockHeight = 0 ' 当前这一块的高
    For ID = 1 To UBound(lines)
        Dim parameters() As String:parameters = Split(lines(ID), "&") ' 解析参数
        Dim newWidth As Double : newWidth = 0' 每一行的宽
        Dim lineHeight As Double:lineHeight = parameters(9) + buffer ' 行高
        For i = 0 To UBound(parameters) Step repeatCount
            ' 创建矩形形状
            Dim shape As shape
            Set shape = ActiveSheet.Shapes.AddShape(msoShapeRoundedRectangle, beginX + newWidth + buffer, fromHeight + buffer + blockHeight, 100, 100)
            ' 设置形状样式和文本
            shape.TextFrame2.TextRange.Font.Size = parameters(i + 9) ' 字号
            shape.TextFrame2.TextRange.text = parameters(i + 11) ' 文本内容
            shape.TextFrame2.VerticalAnchor = msoAnchorMiddle
            shape.TextFrame.AutoSize = True
            ' 设置形状样式和文本
            shape.Fill.ForeColor.RGB = RGB(parameters(i + 3), parameters(i + 4), parameters(i + 5)) ' 设置填充颜色，此处使用红色作为示例
            shape.Line.ForeColor.RGB = RGB(parameters(i + 6), parameters(i + 7), parameters(i + 8)) ' 设置描边颜色，此处使用蓝色作为示例
            shape.Line.Weight = parameters(i + 10) ' 设置描边宽度
            shape.Adjustments.Item(1) = 0.1 ' 圆角角
            ' 为矩形形状创建一个新文本框
            With shape.TextFrame2.TextRange
                With .Font.Fill ' 设置文本颜色，此处使用蓝色作为示例
                    .Visible = msoTrue
                    .ForeColor.RGB = RGB(parameters(i), parameters(i + 1), parameters(i + 2)) ' 字体颜色
                End With
            End With
            ' 调整形状大小以额外留出空白
            shape.Width = shape.Width + buffer
            shape.Height = lineHeight
            newWidth = newWidth + shape.Width
            ' 清空形状以便创建下一个形状
            Set shape = Nothing
        Next i
        blockHeight = blockHeight + lineHeight
        widthOffset = Application.Max(widthOffset, newWidth)
    Next ID
    ' 创建占位符矩形以包含组
    Set wrapShape = ActiveSheet.Shapes.AddShape(msoShapeRoundedRectangle, 0, fromHeight + lineHeight, buffer + widthOffset + buffer, buffer + blockHeight + buffer)
    wrapShape.Fill.ForeColor.RGB = RGB(firstLines(3), firstLines(4), firstLines(5))
    wrapShape.Adjustments.Item(1) = 0.03 '圆角角
    wrapShape.ZOrder msoSendToBack
    fromHeight = fromHeight + buffer + blockHeight + buffer
    Dim textToWrite As String
    textToWrite = "" & fromHeight
    Call WriteToFile(textToWrite)
End Sub

Sub MergeCellsToFitText()
    ' From Python
    Dim text As String : text = ReadFromFile() ' 读取文本内容
    Dim lines() As String : lines = Split(text, "&&") ' 每一行
    ' 第一行的特殊参数
    Dim firstLine As String : firstLine = lines(0) ' 第一行
    Dim firstLines() As String : firstLines = Split(firstLine, "&") ' 切全局参数
    Dim beginX As Integer : beginX = CDbl(firstLines(0)) ' 起始位置
    Dim fromHeight As Double : fromHeight = CDbl(firstLines(1)) ' 起始高
    Dim repeatCount As Integer : repeatCount = CDbl(firstLines(2))  ' 参数的个数
    ' 运行时行列
    Dim lineCount As Integer : lineCount = 0 ' 行数
    Dim lineMergeCount As Integer : lineMergeCount = 1 ' 合并到第几格

    For ID = 1 To UBound(lines)
        Dim parameters() As String : parameters = Split(lines(ID), "&") ' 解析参数
        lineMergeCount = 1
        For i = 0 To UBound(parameters) Step repeatCount
            Dim cell As range
            Set cell = Cells(fromHeight + lineCount, beginX + lineMergeCount)
            cell.Font.Name = "Consolas"
            cell.Font.Size = 12
            cell.NumberFormat = "@"  ' @ 表示纯文本格式
            cell.Value = parameters(i + 6)
            cell.Interior.Color = RGB(parameters(i + 3), parameters(i + 4), parameters(i + 5)) ' 设置单元格的背景颜色
            cell.Font.Color = RGB(parameters(i + 0), parameters(i + 1), parameters(i + 2)) ' 设置单元格文字的颜色
            Dim pixelWidth As Double : pixelWidth = GetTxtLen(parameters(i + 6)) ' 计算文本的像素长度
            Dim mergeCount As Integer : mergeCount = Ceiling(pixelWidth / 16)
            If mergeCount = 0 Then
                mergeCount = 1
            End If
            range(cell, cell.Offset(0, mergeCount - 1)).Merge ' 合并需要的格子范围
            lineMergeCount = lineMergeCount + mergeCount
            cell.Value = parameters(i + 6) ' 在合并后的单元格内插入文本
        Next i
        lineCount = lineCount + 1
    Next ID

    Dim textToWrite As String
    textToWrite = mergeCount & ""
    Call WriteToFile(textToWrite)
End Sub
' 向上取整
Function Ceiling(Byval x As Double) As Integer
    If x > Int(x) Then
        Ceiling = Int(x) + 1
    Else
        Ceiling = Int(x)
    End If
End Function
' 获取文本长度
Function GetTxtLen(text As String)
    ' 设置中文像素宽度和英文数字符号的像素宽度
    Dim chinesePixelWidth As Double : chinesePixelWidth = 12 ' 中文像素宽度
    Dim englishPixelWidth As Double : englishPixelWidth = 7 ' 英文数字符号的像素宽度
    ' 英文和中文个数
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
