' ��ݼ�����

' ����һ����
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
    Selection.Cut ' ��ռ��һ�������
    ActiveSheet.Paste
End Sub

' ��
Sub NormalLine()
    CreateLine (False)
End Sub

' ��ͷ��
Sub ArrowLine()
    CreateLine (True)
End Sub

'ǰһ��Sheet
Sub PrevSheet()
    On Error Resume Next ' �п���û����һ��Sheet
    ActiveSheet.Previous.Select
    On Error Goto 0
End Sub

'��һ��sheet
Sub NextSheet()
    On Error Resume Next ' �п���û����һ��Sheet
    ActiveSheet.Next.Select
    On Error Goto 0
End Sub


' ��������һ��Shape
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
        '��������
        ActiveSheet.Shapes.AddShape(msoShapeRoundedRectangle, 0, 0, wh, wh).Select
        Selection.ShapeRange.Line.Visible = msoFalse
        Selection.ShapeRange.TextFrame2.VerticalAnchor = msoAnchorMiddle
        Selection.ShapeRange.TextFrame2.TextRange.ParagraphFormat.Alignment = msoAlignCenter
        Selection.ShapeRange.TextFrame2.TextRange.Font.Size = 20
        If shp Is Nothing Then 'δѡ��Shape
            Selection.Cut
            ActiveSheet.Paste
        Else
            If shp.AutoShapeType = 1 Then 'ѡPic
                Selection.ShapeRange.IncrementLeft shp.Left - buff
                Selection.ShapeRange.IncrementTop shp.Top - buff
                Selection.ShapeRange.ScaleWidth (shp.Width + buff * 2) / wh, msoFalse, msoScaleFromTopLeft
                Selection.ShapeRange.ScaleHeight (shp.Height + buff * 2) / wh, msoFalse, msoScaleFromTopLeft
                Selection.ShapeRange.Adjustments.Item(1) = 0.03 'Բ��
                Selection.ShapeRange.ZOrder msoSendToBack
            Else 'ѡ��Shape
                Selection.Cut
                ActiveSheet.Paste
            End If
        End If
End Sub