Function ReadFromFile() As String
    Dim filePath As String:filePath = ActiveWorkbook.path & "/PythonToExcel.txt" ' PythonToExcel.txt �ļ���·��
    Dim text As String
    Dim temp As String ' ��ʱ����
    ' ���ı��ļ�����ȡ����
    Open filePath For Input As #1
    Do Until EOF(1)
        Line Input #1, temp
        text = text & temp
    Loop
    Close #1
    Debug.Print text ' ������ Debug.Print ��� text�������滻Ϊ����Ҫ����������
    ReadFromFile = text ' ���ض�ȡ�����ı�����
End Function

Sub WriteToFile(textToWrite As String)
    Dim filePath As String:filePath = ActiveWorkbook.path & "/ExcelToPython.txt" ' ExcelToPython.txt �ļ���·��
    Dim fileNumber As Integer
    fileNumber = FreeFile ' ���ı��ļ�
    Open filePath For Output As #fileNumber
    Print #fileNumber, textToWrite ' ���ı�����д�뵽�ļ�
    Close #fileNumber ' �ر��ı��ļ�
End Sub