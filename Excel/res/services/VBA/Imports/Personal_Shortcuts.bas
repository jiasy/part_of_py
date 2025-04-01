' 快捷键操作

' 创建一条线
Private Sub CreateLine(isArrow As Boolean)
    ActiveSheet.Shapes.AddConnector(msoConnectorStraight, 1819, 425, 1891, 497).Select
    If isArrow Then
        Selection.ShapeRange.Line.EndArrowheadStyle = msoArrowheadTriangle
    End If
    With Selection.ShapeRange.Line
        .Visible = msoTrue
        .Weight = 2
    End With
    With Selection.ShapeRange.Line
        .Visible = msoTrue
        .ForeColor.RGB = RGB(255, 0, 0)
        .Transparency = 0
    End With
    Selection.Cut ' 会占用一格剪贴板
    ActiveSheet.Paste
End Sub

' 线
Sub NormalLine()
    CreateLine (False)
End Sub

' 箭头线
Sub ArrowLine()
    CreateLine (True)
End Sub

'前一个Sheet
Sub PrevSheet()
    On Error Resume Next ' 有可能没有上一个Sheet
    ActiveSheet.Previous.Select
    On Error Goto 0
End Sub

'下一个sheet
Sub NextSheet()
    On Error Resume Next ' 有可能没有上一个Sheet
    ActiveSheet.Next.Select
    On Error Goto 0
End Sub


' 背景垫上一张Shape
Sub TipFrame()
    Dim shp As shape
    On Error Resume Next
    Set shp = ActiveSheet.Shapes(Selection.Name)
    On Error Goto 0
        Dim createShp As shape
        Dim buff As Integer
        Dim wh As Integer
        buff = 10
        wh = 200
        '创建方框
        ActiveSheet.Shapes.AddShape(msoShapeRoundedRectangle, 0, 0, wh, wh).Select
        Selection.ShapeRange.Line.Visible = msoFalse
        Selection.ShapeRange.TextFrame2.VerticalAnchor = msoAnchorMiddle
        Selection.ShapeRange.TextFrame2.TextRange.ParagraphFormat.Alignment = msoAlignCenter
        Selection.ShapeRange.TextFrame2.TextRange.Font.Size = 20
        If shp Is Nothing Then '未选中Shape
            Selection.Cut
            ActiveSheet.Paste
        Else
            If shp.AutoShapeType = 1 Then '选Pic
                Selection.ShapeRange.IncrementLeft shp.Left - buff
                Selection.ShapeRange.IncrementTop shp.Top - buff
                Selection.ShapeRange.ScaleWidth (shp.Width + buff * 2) / wh, msoFalse, msoScaleFromTopLeft
                Selection.ShapeRange.ScaleHeight (shp.Height + buff * 2) / wh, msoFalse, msoScaleFromTopLeft
                Selection.ShapeRange.Adjustments.Item(1) = 0.03 '圆角
                Selection.ShapeRange.ZOrder msoSendToBack
            Else '选中Shape
                Selection.Cut
                ActiveSheet.Paste
            End If
        End If
End Sub