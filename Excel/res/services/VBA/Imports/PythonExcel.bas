Function ReadFromFile() As String
    Dim filePath As String:filePath = ActiveWorkbook.path & "/PythonToExcel.txt" ' PythonToExcel.txt 文件的路径
    Dim text As String
    Dim temp As String ' 临时变量
    ' 打开文本文件并读取内容
    Open filePath For Input As #1
    Do Until EOF(1)
        Line Input #1, temp
        text = text & temp
    Loop
    Close #1
    Debug.Print text ' 这里用 Debug.Print 输出 text，可以替换为你需要的其他操作
    ReadFromFile = text ' 返回读取到的文本内容
End Function

Sub WriteToFile(textToWrite As String)
    Dim filePath As String:filePath = ActiveWorkbook.path & "/ExcelToPython.txt" ' ExcelToPython.txt 文件的路径
    Dim fileNumber As Integer
    fileNumber = FreeFile ' 打开文本文件
    Open filePath For Output As #fileNumber
    Print #fileNumber, textToWrite ' 将文本内容写入到文件
    Close #fileNumber ' 关闭文本文件
End Sub