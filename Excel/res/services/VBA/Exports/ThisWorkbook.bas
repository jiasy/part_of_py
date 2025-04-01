' 当工作簿打开时，设置快捷键
Private Sub Workbook_Open()
    ' 设置快捷键 Ctrl+Shift+1
    Application.OnKey "^+1", "PERSONAL.XLSB!TipFrame"
    Application.OnKey "^+2", "PERSONAL.XLSB!ArrowLine"
    Application.OnKey "^+3", "PERSONAL.XLSB!NormalLine"
    Application.OnKey "^+j", "PERSONAL.XLSB!PrevSheet"
    Application.OnKey "^+l", "PERSONAL.XLSB!NextSheet"
End Sub

' 当工作簿关闭时，清除快捷键
Private Sub Workbook_BeforeClose(Cancel As Boolean)
    Application.OnKey "^+1", ""
    Application.OnKey "^+2", ""
    Application.OnKey "^+3", ""
    Application.OnKey "^+j", ""
    Application.OnKey "^+l", ""
End Sub
