Sub SendEmail()
    Dim OutlookApp As Object
    Dim MyItem As Object
    
    Set OutlookApp = CreateObject("Outlook.Application")
    Set MyItem = OutlookApp.CreateItemFromTemplate("C:\Users\mwx1202039\AppData\Roaming\Microsoft\Templates\【SE工作日报】.oft")
    If Weekday(Now(), vbMonday) = 1 Then
       MyItem.Subject = "【SE工作日报】 梅闯 " & Format(Now() - 3, "YYYY/MM/DD")
    Else
        MyItem.Subject = "【SE工作日报】 梅闯 " & Format(Now() - 1, "YYYY/MM/DD")
    End If
    
    
    
    MyItem.Display
    MyItem.GetInspector.WordEditor.Content.Paste
    
    Set MyItem = Nothing
    Set OutlookApp = Nothing
    
End Sub
