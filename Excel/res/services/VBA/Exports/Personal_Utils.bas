

' 报错用
Sub ShowMsgThenEnd(message As String, Optional title As String = "错误")
    MsgBox message, vbCritical, title
    End
End Sub
    