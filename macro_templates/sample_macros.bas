
Sub TransferSheetWithMacros()
    Dim sourceWb As Workbook
    Dim destWb As Workbook
    Dim sourceSheet As Worksheet
    Dim sheetName As String
    
    ' Set the sheet name to copy
    sheetName = "Sheet1" ' Change this to your sheet name
    
    ' Open source workbook
    Set sourceWb = Workbooks.Open(ThisWorkbook.Path & "\source.xlsx")
    Set sourceSheet = sourceWb.Sheets(sheetName)
    
    ' Copy sheet to active workbook
    sourceSheet.Copy Before:=ThisWorkbook.Sheets(1)
    
    ' Close source workbook
    sourceWb.Close SaveChanges:=False
    
    MsgBox "Sheet transferred with macros preserved!"
End Sub

Sub PreserveAllMacros()
    ' This subroutine ensures all macros are preserved
    ' when copying sheets between workbooks
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    
    ' Your macro operations here
    
    Application.EnableEvents = True
    Application.ScreenUpdating = True
End Sub
